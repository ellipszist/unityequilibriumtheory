import os
import uuid
import json
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import Json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Initialize embedding model (1024 dimensions)
print("Loading embedding model BAAI/bge-m3 (this may take a minute)...")
# BAAI/bge-m3 outputs 1024 dimension vectors which matches our DB schema
model = SentenceTransformer("BAAI/bge-m3")

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

DOCS_DIR = Path(__file__).parent.parent / "Doc"

def get_collection_name(folder_name: str) -> str:
    folder_name = folder_name.lower()
    if "theory" in folder_name:
        return "theory"
    elif "concept" in folder_name:
        return "concept"
    elif "evidence" in folder_name:
        return "evidence"
    elif "manual" in folder_name:
        return "manual"
    elif "overview" in folder_name:
        return "overview"
    return "general"

def ingest_documents():
    print(f"Connecting to database at {DATABASE_URL}...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    total_files = 0
    total_chunks = 0

    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue

            file_path = Path(root) / file
            relative_path = file_path.relative_to(DOCS_DIR)
            folder_name = file_path.parent.name
            
            collection = get_collection_name(folder_name)
            title = file.replace('.md', '').replace('_', ' ')
            slug = str(relative_path).lower().replace('\\', '/').replace('.md', '')
            
            print(f"Processing {relative_path}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                continue

            # Insert document
            doc_id = str(uuid.uuid4())
            metadata = {
                "folder": folder_name,
                "original_file": file
            }

            try:
                cursor.execute("""
                    INSERT INTO documents (id, slug, title, collection, source_path, content, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (slug) DO UPDATE 
                    SET title = EXCLUDED.title,
                        content = EXCLUDED.content,
                        metadata = EXCLUDED.metadata,
                        updated_at = NOW()
                    RETURNING id;
                """, (doc_id, slug, title, collection, str(relative_path).replace('\\', '/'), content, Json(metadata)))
                
                # Fetch actual doc_id (might be existing if conflict)
                actual_doc_id = cursor.fetchone()[0]
                
                # Delete existing chunks for this doc if it was updated
                cursor.execute("DELETE FROM document_chunks WHERE doc_id = %s", (actual_doc_id,))
                
                # Split content into chunks
                chunks = text_splitter.split_text(content)
                
                for idx, chunk in enumerate(chunks):
                    # Generate embedding
                    embedding = model.encode(chunk)
                    embedding_list = embedding.tolist()
                    
                    # Insert chunk
                    cursor.execute("""
                        INSERT INTO document_chunks (doc_id, text, embedding, chunk_index)
                        VALUES (%s, %s, %s, %s)
                    """, (actual_doc_id, chunk, embedding_list, idx))
                    
                    total_chunks += 1
                
                conn.commit()
                total_files += 1
                print(f"  ✓ Indexed {len(chunks)} chunks")
                
            except Exception as e:
                conn.rollback()
                print(f"  ✗ Error processing {file}: {e}")

    cursor.close()
    conn.close()
    print(f"\nIngestion complete! Processed {total_files} files into {total_chunks} chunks.")

if __name__ == "__main__":
    ingest_documents()

"""
Migrate LanceDB table from dynamic list<double> to fixed_size_list<float32>
so that vector search (ANN) works correctly.

Usage:
    python -m research_uet.knowledge_base.migrate_lance_schema
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

import numpy as np
import pyarrow as pa
import lancedb


DB_PATH = Path(__file__).parent / "vectors" / "lance"
TABLE_NAME = "uet_vectors"
SEMANTIC_DIM = 8
UET_DIM = 20


def migrate():
    db = lancedb.connect(str(DB_PATH))

    if TABLE_NAME not in db.table_names():
        print(f"Table '{TABLE_NAME}' not found.")
        return

    old_table = db.open_table(TABLE_NAME)
    row_count = old_table.count_rows()
    print(f"Old table: {row_count} rows")
    print(f"Old schema:\n{old_table.schema}\n")

    # Read all data
    df = old_table.to_pandas()

    # Build explicit PyArrow schema with fixed_size_list for vectors
    schema = pa.schema([
        pa.field("doc_id", pa.string()),
        pa.field("semantic_vec", pa.list_(pa.float32(), SEMANTIC_DIM)),
        pa.field("uet_vec", pa.list_(pa.float32(), UET_DIM)),
        pa.field("text", pa.string()),
        pa.field("topic_id", pa.string()),
        pa.field("topic_number", pa.string()),
        pa.field("file_path", pa.string()),
        pa.field("file_type", pa.string()),
        pa.field("title", pa.string()),
        pa.field("content_hash", pa.string()),
        pa.field("char_count", pa.int64()),
        pa.field("omega", pa.float64()),
        pa.field("kappa", pa.float64()),
        pa.field("beta", pa.float64()),
        pa.field("entropy", pa.float64()),
        pa.field("axiom_count", pa.int64()),
        pa.field("axiom_signature", pa.string()),
        pa.field("scale", pa.string()),
        pa.field("indexed_at", pa.float64()),
    ])

    # Convert vectors to proper format
    sem_vecs = [np.array(v, dtype=np.float32).tolist() for v in df["semantic_vec"]]
    uet_vecs = [np.array(v, dtype=np.float32).tolist() for v in df["uet_vec"]]

    # Build PyArrow table with explicit schema (skip metadata column)
    arrays = [
        pa.array(df["doc_id"].tolist(), type=pa.string()),
        pa.FixedSizeListArray.from_arrays(pa.array([x for row in sem_vecs for x in row], type=pa.float32()), SEMANTIC_DIM),
        pa.FixedSizeListArray.from_arrays(pa.array([x for row in uet_vecs for x in row], type=pa.float32()), UET_DIM),
        pa.array(df["text"].tolist(), type=pa.string()),
        pa.array(df["topic_id"].tolist(), type=pa.string()),
        pa.array(df["topic_number"].tolist(), type=pa.string()),
        pa.array(df["file_path"].tolist(), type=pa.string()),
        pa.array(df["file_type"].tolist(), type=pa.string()),
        pa.array(df["title"].tolist(), type=pa.string()),
        pa.array(df["content_hash"].tolist(), type=pa.string()),
        pa.array(df["char_count"].tolist(), type=pa.int64()),
        pa.array(df["omega"].tolist(), type=pa.float64()),
        pa.array(df["kappa"].tolist(), type=pa.float64()),
        pa.array(df["beta"].tolist(), type=pa.float64()),
        pa.array(df["entropy"].tolist(), type=pa.float64()),
        pa.array(df["axiom_count"].tolist(), type=pa.int64()),
        pa.array(df["axiom_signature"].tolist(), type=pa.string()),
        pa.array(df["scale"].tolist(), type=pa.string()),
        pa.array(df["indexed_at"].tolist(), type=pa.float64()),
    ]
    arrow_table = pa.table(arrays, schema=schema)

    # Drop old table
    db.drop_table(TABLE_NAME)
    print("Dropped old table.")

    # Create new table with explicit vector schema
    new_table = db.create_table(TABLE_NAME, arrow_table)
    print(f"\nNew table: {new_table.count_rows()} rows")
    print(f"New schema:\n{new_table.schema}")

    # Verify vector search works
    query_uet = np.zeros(UET_DIM, dtype=np.float32)
    query_uet[0] = 1.0
    try:
        results = new_table.search(query_uet, vector_column_name="uet_vec").limit(3).to_list()
        print(f"\nVector search test: OK — {len(results)} results returned")
        for r in results[:3]:
            print(f"  {r['doc_id']} (distance: {r['_distance']:.4f})")
    except Exception as e:
        print(f"\nVector search test FAILED: {e}")
        return

    print(f"\n✅ Migration complete! {row_count} rows migrated.")


if __name__ == "__main__":
    migrate()

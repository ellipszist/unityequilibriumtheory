import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from .executive_router import ExecutiveRouter
from .semantic_engine import UETSemanticEngine

app = FastAPI(title="UET Semantic Engine API")
engine = UETSemanticEngine()
router = ExecutiveRouter(engine)

# Expose models
class ChatRequest(BaseModel):
    prompt: str
    doc_context: Optional[str] = None
    session_id: Optional[str] = None
    project_scope: Optional[str] = None
    source_tags: Optional[list[str]] = None

class IngestRequest(BaseModel):
    doc_id: str
    text: str
    source_type: Optional[str] = "text"
    project_scope: Optional[str] = None
    doc_version: Optional[str] = None
    tags: Optional[list[str]] = None
    ingest_mode: Optional[str] = "manual"

class ComputeResult(BaseModel):
    response: str
    equilibrium_data: Dict[str, Any]
    work_computed: float
    task_type: Optional[str] = None
    session_id: Optional[str] = None

@app.post("/ingest")
async def ingest_document(req: IngestRequest):
    """Ingest a document into the UET Semantic Manifold"""
    router.ingest_document(
        doc_id=req.doc_id,
        text=req.text,
        source_type=req.source_type or "text",
        project_scope=req.project_scope,
        doc_version=req.doc_version,
        tags=req.tags,
        ingest_mode=req.ingest_mode or "manual",
    )
    return {"status": "success", "message": f"Ingested {len(req.text)} chars for {req.doc_id}"}

@app.post("/chat", response_model=ComputeResult)
async def chat(req: ChatRequest):
    """
    1. Calculate Equilibrium Path (Work)
    2. Generate Response based on Path
    """
    if len(engine.knowledge_chunks) == 0 and req.doc_context:
        router.ingest_document("temp_context", req.doc_context)

    result = router.handle_chat(
        prompt=req.prompt,
        doc_context=req.doc_context,
        session_id=req.session_id,
        project_scope=req.project_scope,
        source_tags=req.source_tags,
    )
    
    return ComputeResult(
        response=result.response,
        equilibrium_data=result.equilibrium_data,
        work_computed=result.work_computed,
        task_type=result.task_type,
        session_id=result.session_id,
    )

@app.get("/debug/status")
async def debug_status():
    return {
        "status": "ok",
        "knowledge_chunk_count": len(engine.knowledge_chunks),
        "vocab_size": len(engine.vocab),
    }

@app.get("/debug/session/{session_id}")
async def debug_session(session_id: str):
    return router.debug_session(session_id)

def start_server(port: int = 8001):
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start_server()

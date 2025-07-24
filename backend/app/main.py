from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from dotenv import load_dotenv
import os

from app.vector_store import TableSemanticIndexer
from app.db_pool import get_attached_engine
from app.sql_agent import make_sql_agent

load_dotenv()

app = FastAPI()
vector_indexer = TableSemanticIndexer()

class QueryRequest(BaseModel):
    question: str
    db_hint: Optional[str] = None
    schema: Optional[str] = None  # Add schema as alternative parameter

@app.on_event("startup")
def startup():
    engine = get_attached_engine()
    vector_indexer.index_table_names(['zepto', 'blinkit', 'instamart'], {"all": engine})

@app.post("/ask-sql")
def ask_sql(req: QueryRequest):
    try:
        # Pick schema from hint or RAG
        schema_name = req.db_hint or req.schema
        if not schema_name:
            docs, metas = vector_indexer.query(req.question)
            schema_name = metas[0]["db"] if metas else "zepto"
        
        # Use single engine, but pass selected schema_name
        agent = make_sql_agent("all", schema=schema_name)
        # Use invoke method instead of run for newer LangChain versions
        response = agent.invoke({"input": req.question})
        return {
            "db": schema_name,
            "answer": response.get("output", ""),
            "intermediate_steps": response.get("intermediate_steps", [])
        }
    except ValueError as e:
        # Handle API key or configuration errors
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "E-commerce SQL Agent API", "status": "running"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        engine = get_attached_engine()
        return {"status": "healthy", "databases": ["zepto", "blinkit", "instamart"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

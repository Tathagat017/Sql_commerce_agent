from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from dotenv import load_dotenv
import os

from app.vector_store import TableSemanticIndexer
from app.db_pool import get_attached_engine
from app.sql_agent import make_sql_agent
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_indexer = TableSemanticIndexer()

class QueryRequest(BaseModel):
    question: str
    db_hint: Optional[str] = None
    schema_name: Optional[str] = None  # Renamed from 'schema' to avoid BaseModel conflict

@app.on_event("startup")
def startup():
    engine = get_attached_engine()
    vector_indexer.index_table_names(['zepto', 'blinkit', 'instamart'], {"all": engine})

@app.post("/ask-sql")
def ask_sql(req: QueryRequest):
    try:
        # Pick schema from hint or RAG
        schema_name = req.db_hint or req.schema_name
        if not schema_name:
            docs, metas = vector_indexer.query(req.question)
            schema_name = metas[0]["db"] if metas else "zepto"
        
        # Debug: Check API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise HTTPException(
                status_code=500, 
                detail="OpenAI API key not configured. Please check your .env file."
            )
        
        # Use single engine, but pass selected schema_name
        agent = make_sql_agent("all", schema=schema_name)
        # Use invoke method instead of run for newer LangChain versions
        response = agent.invoke({"input": req.question})
        
        # Extract SQL query from intermediate steps
        executed_sql = None
        intermediate_steps = response.get("intermediate_steps", [])
        
        # Helper function to extract SQL from various formats
        def extract_sql_from_text(text):
            import re
            sql_patterns = [
                # Pattern for JSON-like format: {"query": "SELECT ..."}
                r'["\']?query["\']?\s*:\s*["\']([^"\']*(?:SELECT|INSERT|UPDATE|DELETE|WITH)[^"\']*)["\']',
                # Pattern for direct SQL statements
                r'\b((?:SELECT|INSERT|UPDATE|DELETE|WITH)\b[^;]*(?:;|$))',
                # Pattern for SQL in action input
                r'Action Input:\s*["\']?([^"\']*(?:SELECT|INSERT|UPDATE|DELETE|WITH)[^"\']*)["\']?',
                # Pattern for SQL in tool input
                r'tool_input["\']?\s*:\s*["\']([^"\']*(?:SELECT|INSERT|UPDATE|DELETE|WITH)[^"\']*)["\']',
            ]
            
            for pattern in sql_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match else ""
                    match = match.strip()
                    if match and len(match) > 10:  # Basic validation
                        return match
            return None
        
        # Look for SQL query in intermediate steps
        for step in intermediate_steps:
            if isinstance(step, tuple) and len(step) >= 2:
                action, observation = step
                
                # Method 1: Check tool name and tool_input
                if hasattr(action, 'tool') and 'sql' in str(action.tool).lower():
                    if hasattr(action, 'tool_input'):
                        tool_input = action.tool_input
                        if isinstance(tool_input, dict) and 'query' in tool_input:
                            executed_sql = tool_input['query']
                            break
                        elif isinstance(tool_input, str):
                            sql = extract_sql_from_text(tool_input)
                            if sql:
                                executed_sql = sql
                                break
                
                # Method 2: Check action log
                if hasattr(action, 'log'):
                    sql = extract_sql_from_text(str(action.log))
                    if sql:
                        executed_sql = sql
                        break
                
                # Method 3: Check full action string representation
                action_str = str(action)
                sql = extract_sql_from_text(action_str)
                if sql:
                    executed_sql = sql
                    break
        
        # Clean up the SQL query if found
        if executed_sql:
            executed_sql = executed_sql.strip()
            # Remove any trailing quotes or brackets
            executed_sql = executed_sql.strip('\'"[]{}')
            # Ensure it ends properly
            if not executed_sql.endswith(';'):
                executed_sql += ';' if executed_sql else ''
        
        return {
            "db": schema_name,
            "answer": response.get("output", ""),
            "sql_query": executed_sql or "No SQL query found in execution steps",
            "intermediate_steps": intermediate_steps
        }
    except ValueError as e:
        # Handle API key or configuration errors
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle other errors
        import traceback
        error_details = f"Error processing request: {str(e)}\n{traceback.format_exc()}"
        print(error_details)  # Log to console for debugging
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

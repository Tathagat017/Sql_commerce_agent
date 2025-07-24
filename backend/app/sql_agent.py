from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
import os
from sqlalchemy import text
from dotenv import load_dotenv

from app.db_pool import get_attached_engine

# Ensure environment variables are loaded
load_dotenv()

def get_attached_tables_info(engine):
    """Get comprehensive table information for all attached databases"""
    tables_info = []
    table_names = []
    
    with engine.connect() as conn:
        # Get list of attached databases
        result = conn.execute(text("PRAGMA database_list;"))
        databases = [row[1] for row in result if row[1] != 'temp']
        
        for db_name in databases:
            if db_name == 'main':
                # Skip main database if empty
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"))
                main_tables = [row[0] for row in result]
                if not main_tables:
                    continue
                tables_to_process = [(table, None) for table in main_tables]
            else:
                # For attached databases
                result = conn.execute(text(f"SELECT name FROM {db_name}.sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"))
                tables_to_process = [(row[0], db_name) for row in result]
            
            # Get table info for each table
            for table_name, schema in tables_to_process:
                try:
                    full_table_name = f"{schema}.{table_name}" if schema else table_name
                    table_names.append(full_table_name)
                    
                    if schema:
                        result = conn.execute(text(f"PRAGMA {schema}.table_info({table_name});"))
                    else:
                        result = conn.execute(text(f"PRAGMA table_info({table_name});"))
                    
                    columns = []
                    for row in result:
                        col_name = row[1]
                        col_type = row[2] or "TEXT"
                        columns.append(f"{col_name} {col_type}")
                    
                    if columns:
                        table_info = f"CREATE TABLE {full_table_name} (\n  {', '.join(columns)}\n);"
                        tables_info.append(table_info)
                        
                        # Add sample data
                        try:
                            sample_result = conn.execute(text(f"SELECT * FROM {full_table_name} LIMIT 3;"))
                            sample_data = [str(row) for row in sample_result]
                            if sample_data:
                                tables_info.append(f"-- Sample data from {full_table_name}:")
                                for sample in sample_data:
                                    tables_info.append(f"-- {sample}")
                        except:
                            pass  # Skip sample data if there's an error
                            
                except Exception as e:
                    print(f"Error getting info for table {table_name}: {e}")
    
    return table_names, "\n\n".join(tables_info)

def make_sql_agent(db_name: str, schema: str = None):
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        raise ValueError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable. "
            "You can get an API key from https://platform.openai.com/api-keys"
        )
    
    engine = get_attached_engine()
    
    # Get table information for attached databases
    table_names, table_info = get_attached_tables_info(engine)
    print(f"Found tables: {table_names}")
    
    # Create basic SQLDatabase and manually override its table info
    db = SQLDatabase(engine)
    
    # Monkey patch the methods to return our attached database information
    db.get_usable_table_names = lambda: table_names
    db.get_table_info = lambda table_names=None: table_info
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"), 
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
        api_key=api_key
    )
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    # Use the default prompt for tool-calling agent type
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type="tool-calling",  # Use tool-calling agent type as recommended
        verbose=True,
        top_k=10,
        max_iterations=15
    )
    return agent

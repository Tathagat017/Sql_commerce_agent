import os
from langchain_openai import OpenAIEmbeddings
import chromadb
from sqlalchemy import inspect

class TableSemanticIndexer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.chroma = chromadb.Client()
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
        self.collection = self.chroma.create_collection("table_names")

    def index_table_names(self, db_names, engines):
        engine = engines["all"]
        insp = inspect(engine)
        for db_name in db_names:
            for table in insp.get_table_names(schema=db_name):
                doc = f"{db_name}.{table}"
                emb = self.embeddings.embed_query(table)
                self.collection.add(
                    ids=[f"{db_name}.{table}"],
                    documents=[doc],
                    embeddings=[emb],
                    metadatas=[{"db": db_name, "table": table}]
                )

    def query(self, query: str, n: int = 3):
        emb = self.embeddings.embed_query(query)
        results = self.collection.query(embeddings=[emb], n_results=n)
        return results["documents"], results["metadatas"]

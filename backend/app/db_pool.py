from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATHS = {
    "zepto": os.path.join(BASE_DIR, "zepto.db"),
    "blinkit": os.path.join(BASE_DIR, "blinkit.db"),
    "instamart": os.path.join(BASE_DIR, "instamart.db"),
}

_engine = None

def get_engine() -> Engine:
    """
    Get a single SQLAlchemy engine with all three databases attached.
    Enables cross-database queries like:
    SELECT * FROM zepto.products UNION ALL SELECT * FROM blinkit.products
    """
    global _engine
    if _engine is None:
        _engine = create_engine(
            "sqlite://",
            poolclass=QueuePool,
            connect_args={"check_same_thread": False},
            pool_size=5,
            max_overflow=10,
        )
        with _engine.connect() as conn:
            for db_name, db_path in DB_PATHS.items():
                if os.path.exists(db_path):
                    attach_sql = f"ATTACH DATABASE '{db_path}' AS {db_name};"
                    conn.execute(text(attach_sql))
                else:
                    raise FileNotFoundError(f"Database file not found: {db_path}")
    return _engine

def get_attached_engine() -> Engine:
    """Alias for get_engine()."""
    return get_engine()

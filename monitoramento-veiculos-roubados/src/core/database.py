import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# DATABASE_URL pode ser algo como:
# - sqlite:///./data.db
# - postgresql+psycopg2://user:password@host:5432/dbname
# - mysql+pymysql://user:password@host:3306/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# Parâmetros especiais para SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency do FastAPI que entrega uma sessão de banco e garante o close()."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./gradebook.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    # Open a new session for this request
    db = SessionLocal()
    try:
        # Lend the session to the endpoint; the function pauses here
        yield db
    finally:
        # Always runs after the request, even if it crashed, so the session is closed
        db.close()
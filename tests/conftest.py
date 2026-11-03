import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Loading models registers your table definitions (like Student) with Base
import models
# Your real FastAPI app, the same one uvicorn runs
from app import app
# Base knows all your tables; get_db is the function we will swap out
from database import Base, get_db

# A separate database file, so your real gradebook.db is never touched
TEST_DATABASE_URL = "sqlite:///./test.db"

# The connection to the test database (same idea as `engine` in database.py)
# check_same_thread=False is needed because TestClient uses more than one thread
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

# A factory that makes sessions talking to the test database
TestSessionLocal = sessionmaker(bind=test_engine)


# A copy of get_db that lends out a TEST database session instead of a real one
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# A fixture: pytest runs this around any test that asks for "db_tables" by name
@pytest.fixture
def db_tables():
    # Before the test: create every table (students etc.) in the test database
    Base.metadata.create_all(bind=test_engine)
    # Pause here while the test runs
    yield
    # After the test: delete all the tables, so the next test starts empty
    Base.metadata.drop_all(bind=test_engine)


# A fixture that gives a test a fake browser wired to the test database
# Asking for db_tables here means the tables exist before the client is used
@pytest.fixture
def client(db_tables):
    # Whenever the app asks for get_db, give it override_get_db instead
    app.dependency_overrides[get_db] = override_get_db
    # Hand the test a TestClient pointed at your real app, then pause
    yield TestClient(app)
    # After the test: remove the swap so the app goes back to normal
    app.dependency_overrides.clear()
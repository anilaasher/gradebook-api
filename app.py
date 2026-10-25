# FastAPI: the framework, and the CORS tool that lets the React page call this API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Our own files
from database import engine, Base
import models  # loads the table classes, so create_all knows which tables to build
from routers import students

# Create gradebook.db and its tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Only the frontend's addresses may call this API from a browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500", "http://localhost:5500",   # old HTML page
        "http://127.0.0.1:5173", "http://localhost:5173",   # React app
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Plug in the student endpoints from routers/students.py
app.include_router(students.router)
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal, Base
from models import Student, Grade

# Create gradebook.db and its tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Only the frontend's addresses may call this API from a browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/students/{name}")
def add_student(name: str):
    # Save a new student to the database
    db = SessionLocal()
    db.add(Student(name=name))
    db.commit()
    db.close()
    return {"message": f"Added {name}"}


@app.get("/students")
def list_students():
    # Return the names of all students
    db = SessionLocal()
    students = db.query(Student).all()
    db.close()
    return {"students": [s.name for s in students]}


@app.post("/students/{name}/grades")
def add_grade(name: str, score: float = Query(ge=0, le=100)):
    # Save a grade (0-100) linked to an existing student
    db = SessionLocal()
    student = db.query(Student).filter(Student.name == name).first()
    if student is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"{name} not found")
    db.add(Grade(score=score, student_id=student.id))
    db.commit()
    db.close()
    return {"message": f"Added grade {score} for {name}"}


@app.get("/students/{name}")
def get_student(name: str):
    # Return a student's grades and their average
    db = SessionLocal()
    student = db.query(Student).filter(Student.name == name).first()
    if student is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"{name} not found")
    grades = db.query(Grade).filter(Grade.student_id == student.id).all()
    scores = [g.score for g in grades]
    # Average only if there are grades, otherwise None (avoids dividing by zero)
    average = sum(scores) / len(scores) if scores else None
    db.close()
    return {"name": name, "grades": scores, "average": average}
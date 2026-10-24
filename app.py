# Depends lets an endpoint ask FastAPI to provide something, such as a session
from fastapi import FastAPI, HTTPException, Query, Depends

from fastapi.middleware.cors import CORSMiddleware
# get_db is the function that opens and closes a session for each request
from database import engine, SessionLocal, Base, get_db
from models import Student, Grade
# Session is only a type label, so VS Code can help with the `db` variable
from sqlalchemy.orm import Session


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


@app.post("/students/{name}")
def add_student(name: str, db: Session = Depends(get_db)):
    # Save a new student; FastAPI opens and closes the session for us
    db.add(Student(name=name))
    db.commit()
    return {"message": f"Added {name}"}


@app.get("/students")
def list_students(db: Session = Depends(get_db)):
    # `db` is a session that FastAPI opened for us and will close afterwards
    students = db.query(Student).all()
    # Send back just the names, as a list
    return {"students": [s.name for s in students]}


@app.post("/students/{name}/grades")
def add_grade(name: str, score: float = Query(ge=0, le=100), db: Session = Depends(get_db)):
    # Find the student the grade belongs to
    student = db.query(Student).filter(Student.name == name).first()
    if student is None:
        raise HTTPException(status_code=404, detail=f"{name} not found")
    # Save the grade, linked to the student by id
    db.add(Grade(score=score, student_id=student.id))
    db.commit()
    return {"message": f"Added grade {score} for {name}"}


@app.get("/students/{name}")
def get_student(name: str, db: Session = Depends(get_db)):
    # Find the student by name
    student = db.query(Student).filter(Student.name == name).first()
    if student is None:
        # No db.close() needed any more, even when we stop early with an error
        raise HTTPException(status_code=404, detail=f"{name} not found")

    # Collect their grades and work out the average
    grades = db.query(Grade).filter(Grade.student_id == student.id).all()
    scores = [g.score for g in grades]
    # Average only if there are grades, otherwise None (avoids dividing by zero)
    average = sum(scores) / len(scores) if scores else None
    return {"name": name, "grades": scores, "average": average}

@app.delete("/students/{name}")
def delete_student(name: str, db: Session = Depends(get_db)):
    # Find the student to remove
    student = db.query(Student).filter(Student.name == name).first()
    if student is None:
        raise HTTPException(status_code=404, detail=f"{name} not found")
    # Delete their grades first, then the student, so no orphan grades are left behind
    db.query(Grade).filter(Grade.student_id == student.id).delete()
    db.delete(student)
    db.commit()
    return {"message": f"Deleted {name}"}
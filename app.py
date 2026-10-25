# Depends lets an endpoint ask FastAPI to provide something, such as a session
from fastapi import FastAPI, HTTPException,  Depends

# FastAPI: the framework, plus Depends for things FastAPI provides to endpoints
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
# IntegrityError is raised when the database refuses a save, e.g. a duplicate name
from sqlalchemy.exc import IntegrityError
# Session is only a type label, so VS Code can help with the `db` variable
from sqlalchemy.orm import Session

# Our own files
from database import engine, Base, get_db
from models import Student, Grade
from schemas import StudentCreate,GradeCreate


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
def get_student_or_404(name: str, db: Session = Depends(get_db)) -> Student:
    # `name` is read from the {name} part of the address
    student = db.query(Student).filter(Student.name == name).first()
    if student is None:
        # The one place in the app that answers "student not found"
        raise HTTPException(status_code=404, detail=f"{name} not found")
    return student

@app.post("/students", status_code=201)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    # FastAPI has already checked `student` against the schema before this runs
    try:
        db.add(Student(name=student.name))
        db.commit()
    except IntegrityError:
        # The database refused a duplicate name: undo the failed save first
        db.rollback()
        # 409 = conflict with something that already exists
        raise HTTPException(status_code=409, detail=f"{student.name} already exists")
    return {"message": f"Added {student.name}"}





@app.get("/students")
def list_students(db: Session = Depends(get_db)):
    # `db` is a session that FastAPI opened for us and will close afterwards
    students = db.query(Student).all()
    # Send back just the names, as a list
    return {"students": [s.name for s in students]}




@app.post("/students/{name}/grades", status_code=201)
def add_grade(
    grade: GradeCreate,
    student: Student = Depends(get_student_or_404),
    db: Session = Depends(get_db),
):
    # `grade` was read from the JSON body and checked against GradeCreate
    # `student` was found by the dependency, or the request stopped with a 404
    db.add(Grade(score=grade.score, student_id=student.id))
    db.commit()
    return {"message": f"Added grade {grade.score} for {student.name}"}

@app.get("/students/{name}")
def get_student(student: Student = Depends(get_student_or_404), db: Session = Depends(get_db)):
    # `student` has already been found, or the request stopped with a 404
    grades = db.query(Grade).filter(Grade.student_id == student.id).all()
    scores = [g.score for g in grades]
    # Average only if there are grades, otherwise None (avoids dividing by zero)
    average = sum(scores) / len(scores) if scores else None
    return {"name": student.name, "grades": scores, "average": average}

@app.delete("/students/{name}")
def delete_student(student: Student = Depends(get_student_or_404), db: Session = Depends(get_db)):
    # Delete their grades first, then the student, so no orphan grades are left behind
    db.query(Grade).filter(Grade.student_id == student.id).delete()
    db.delete(student)
    db.commit()
    return {"message": f"Deleted {student.name}"}


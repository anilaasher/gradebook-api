# Every endpoint whose address starts with /students
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_student_or_404
from models import Student, Grade
from schemas import StudentCreate, GradeCreate

# prefix: "/students" is added in front of every path below
# tags: groups these endpoints together in /docs
router = APIRouter(prefix="/students", tags=["students"])


@router.post("", status_code=201)
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


@router.get("")
def list_students(db: Session = Depends(get_db)):
    # Send back just the names, as a list
    students = db.query(Student).all()
    return {"students": [s.name for s in students]}


@router.get("/{name}")
def get_student(student: Student = Depends(get_student_or_404), db: Session = Depends(get_db)):
    # `student` has already been found, or the request stopped with a 404
    grades = db.query(Grade).filter(Grade.student_id == student.id).all()
    scores = [g.score for g in grades]
    # Average only if there are grades, otherwise None (avoids dividing by zero)
    average = sum(scores) / len(scores) if scores else None
    return {"name": student.name, "grades": scores, "average": average}


@router.post("/{name}/grades", status_code=201)
def add_grade(
    grade: GradeCreate,
    student: Student = Depends(get_student_or_404),
    db: Session = Depends(get_db),
):
    # `grade` was read from the JSON body and checked against GradeCreate
    db.add(Grade(score=grade.score, student_id=student.id))
    db.commit()
    return {"message": f"Added grade {grade.score} for {student.name}"}


@router.delete("/{name}")
def delete_student(student: Student = Depends(get_student_or_404), db: Session = Depends(get_db)):
    # Delete their grades first, then the student, so no orphan grades are left behind
    db.query(Grade).filter(Grade.student_id == student.id).delete()
    db.delete(student)
    db.commit()
    return {"message": f"Deleted {student.name}"}
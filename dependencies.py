# Helpers that endpoints ask FastAPI to provide, using Depends(...)
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Student


def get_student_or_404(name: str, db: Session = Depends(get_db)) -> Student:
    # `name` is read from the {name} part of the address
    student = db.query(Student).filter(Student.name == name).first()
    if student is None:
        # The one place in the app that answers "student not found"
        raise HTTPException(status_code=404, detail=f"{name} not found")
    return student
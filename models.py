from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    score = Column(Float)
    student_id = Column(Integer, ForeignKey("students.id"))
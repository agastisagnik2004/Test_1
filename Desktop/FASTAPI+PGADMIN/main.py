from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal, engine
from model import Student

# Create table
Student.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request schema
class StudentCreate(BaseModel):
    name: str
    age: int
    department: str

# ---------------- CREATE ----------------
@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name=student.name,
        age=student.age,
        department=student.department
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# ---------------- READ ALL ----------------
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

# ---------------- READ ONE ----------------
@app.get("/students/{id}")
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ---------------- UPDATE ----------------
@app.put("/students/{id}")
def update_student(id: int, student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.name = student.name
    db_student.age = student.age
    db_student.department = student.department

    db.commit()
    db.refresh(db_student)
    return db_student

# ---------------- DELETE ----------------
@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Deleted successfully"}

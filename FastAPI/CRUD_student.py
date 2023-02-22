from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector

# kết nối cơ sở dữ liệu
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="mydb"
)

app = FastAPI()

class Student(BaseModel):
    id: int
    name: str
    address: str = None
    phone: str = None

mycursor = mydb.cursor()

# CREATE
@app.post("/students")
async def create_student(student: Student):
    sql = "INSERT INTO student (id, name, address, phone) VALUES (%s, %s, %s, %s)"
    val = (student.id, student.name, student.address, student.phone)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Student created successfully"}

# GET
@app.get("/students", response_model=List[Student])
async def read_students():
    sql = "SELECT * FROM student"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    students = []
    for result in results:
        student = Student(id=result[0], name=result[1], address=result[2], phone=result[3])
        students.append(student)
    return students

# GET BY ID
@app.get("/students/{student_id}", response_model=Student)
async def read_student(student_id: int):
    sql = "SELECT * FROM student WHERE id = %s"
    val = (student_id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student = Student(id=result[0], name=result[1], address=result[2], phone=result[3])
    return student


# UPDATE
@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    sql = "UPDATE student SET name = %s, address = %s, phone = %s WHERE id = %s"
    val = (student.name, student.address, student.phone, student_id)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}

# DELETE
@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    sql = "DELETE FROM student WHERE id = %s"
    val = (student_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student removed successfully"}
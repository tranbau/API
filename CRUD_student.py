from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
from typing import Union
# connect to MySQL
mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   database="mydb"
)
mycursor = mydb.cursor()

# create table student
mycursor.execute("""
                CREATE TABLE student(
                    id integer  auto_increment primary key,
                    name varchar(255) not null,
                    address varchar(255),
                    phone varchar(255)
                 )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
                 """)

class Student(BaseModel):
    id: int
    name: str
    address: Union[str, None] = None
    phone: Union[str, None] = None
    
# CRUD APIs
app = FastAPI()
# Create
@app.post("/create_student")
async def create_student(student: Student):
    mycursor = mydb.cursor()
    sql = "insert into student(name, address, phone) values (%s, %s, %s)"
    val = (student.name, student.address, student.phone)
    mycursor.execute(sql, val)    
    mydb.commit()
    return {"message": "Student created successfully"}


# Read
@app.get("/read_student")
async def read_student():
    mycursor = mydb.cursor()
    sql = "select * from student"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

@app.get("/read_student/{student_id}")
async def read_student(student_id: int):
    mycursor = mydb.cursor()
    sql = "select * from student where id = %s"
    val = (student_id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult

# Update
@app.put("/update_student/{student_id}")
async def update_student(student_id: int,student: Student):
    mycursor = mydb.cursor()
    sql = "update student set name = %s, address = %s, phone = %s where id = %s"
    val = [student.name, student.address, student.phone, student_id]
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Student updated successfully"}

# Delete
@app.delete("/delete_student/{student_id}")
async def delete_student(student_id: int):
    mycursor = mydb.cursor()
    sql = "Delete from student where id = %s"
    val = (student_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return  {"message": "Student removed successfully"}
    
    
    

        
    
    




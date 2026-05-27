import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="860560",
    database="face_attendance"
)

cursor = db.cursor()

student_id = int(input("Enter ID: "))
name = input("Enter Name: ")
department = input("Enter Department: ")

query = "INSERT INTO students (id, name, department) VALUES (%s, %s, %s)"
values = (student_id, name, department)

cursor.execute(query, values)

db.commit()

print("Student Added Successfully")
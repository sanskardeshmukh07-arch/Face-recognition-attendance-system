import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="860560",
    database="face_attendance"
)

cursor = db.cursor()

print("Database Connected Successfully")
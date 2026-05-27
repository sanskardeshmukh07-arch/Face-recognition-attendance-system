import cv2
import numpy as np
import os
from datetime import datetime
import mysql.connector

print("Starting Attendance System...")

# =========================
# DATABASE CONNECTION
# =========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="860560",
    database="face_attendance"
)

cursor = db.cursor()

# =========================
# LOAD FACE RECOGNIZER
# =========================
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# =========================
# LOAD HAARCASCADE
# =========================
faceCascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

# =========================
# FONT
# =========================
font = cv2.FONT_HERSHEY_SIMPLEX

# =========================
# LOAD STUDENTS FROM MYSQL
# =========================
names = {}

cursor.execute("SELECT id, name FROM students")

students = cursor.fetchall()

for student in students:
    student_id = student[0]
    student_name = student[1]

    names[student_id] = student_name

print("Students Loaded Successfully")

# =========================
# START CAMERA
# =========================
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Camera not opening ❌")
    exit()

print("Camera started ✅")

# =========================
# PREVENT DUPLICATE ATTENDANCE
# =========================
marked_attendance = set()

# =========================
# =========================
# SUBJECT NAME FROM GUI
# =========================
subject_name = os.environ.get(
    "SUBJECT_NAME",
    "Compiler Design"
)

print(f"Selected Subject: {subject_name}")
# =========================
# FACE RECOGNITION LOOP
# =========================
while True:

    ret, img = cam.read()

    if not ret:
        print("Failed to read camera")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect Faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        # Draw Rectangle
        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Predict Face
        id, confidence = recognizer.predict(
            gray[y:y+h, x:x+w]
        )

        # LOWER CONFIDENCE = BETTER MATCH
        if confidence < 40:

            name = names.get(id, "Unknown")

            # MARK ATTENDANCE ONLY ONCE
            if name != "Unknown" and name not in marked_attendance:

                now = datetime.now()

                # MYSQL DATE FORMAT
                date_string = now.strftime("%Y-%m-%d")

                # MYSQL TIME FORMAT
                time_string = now.strftime("%H:%M:%S")

                # =========================
                # INSERT ATTENDANCE INTO MYSQL
                # =========================
                query = """
                INSERT INTO attendance
                (student_id, name, subject, date, time)
                VALUES (%s, %s, %s, %s, %s)
                """

                values = (
                    id,
                    name,
                    subject_name,
                    date_string,
                    time_string
                )

                cursor.execute(query, values)
                db.commit()

                marked_attendance.add(name)

                print(f"Attendance marked for {name}")

        else:
            name = "Unknown"

        # =========================
        # DISPLAY NAME
        # =========================
        cv2.putText(
            img,
            str(name),
            (x, y - 10),
            font,
            1,
            (255, 255, 255),
            2
        )

        # =========================
        # DISPLAY CONFIDENCE
        # =========================
        cv2.putText(
            img,
            f"Confidence: {round(confidence, 2)}",
            (x, y + h + 25),
            font,
            0.7,
            (0, 255, 255),
            2
        )

    # =========================
    # SHOW CAMERA WINDOW
    # =========================
    cv2.imshow(
        "Face Attendance System",
        img
    )

    # ESC KEY TO EXIT
    key = cv2.waitKey(10) & 0xff

    if key == 27:
        break

# =========================
# CLEANUP
# =========================
cam.release()
cv2.destroyAllWindows()

print("Attendance System Closed")
import cv2
import os
import csv

# Open Camera
cam = cv2.VideoCapture(0)
print("Camera Open:", cam.isOpened())

# Load Haarcascade
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
print("Cascade Loaded:", not face_detector.empty())

# Create dataset folder if not exists
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# Take user input
face_id = input("Enter Student ID: ")
name = input("Enter Name: ")

# Save ID + Name in CSV
file_exists = os.path.isfile("names.csv")

with open("names.csv", "a", newline='') as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["ID", "Name"])

    writer.writerow([face_id, name])

print("Name saved successfully!")

count = 0

while True:
    ret, img = cam.read()

    if not ret:
        print("Failed to grab image")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Better face detection
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        count += 1

        # Crop face properly
        face = gray[y:y+h, x:x+w]

        # Save face image
        file_name = f"dataset/User.{face_id}.{count}.jpg"
        cv2.imwrite(file_name, face)

        # Draw rectangle
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Show count on screen
        cv2.putText(
            img,
            f"Images Captured: {count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Small delay for better variation
        cv2.waitKey(100)

    cv2.imshow('Register Face', img)

    # Press ESC OR capture 100 images
    if cv2.waitKey(1) == 27 or count >= 100:
        break

cam.release()
cv2.destroyAllWindows()

print("Face data collected successfully!")
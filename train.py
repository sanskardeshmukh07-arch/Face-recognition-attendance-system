import cv2
import numpy as np
from PIL import Image
import os

# -------- Path -------- #
dataset_path = 'dataset'

# -------- Create LBPH Recognizer -------- #
recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=2,
    neighbors=8,
    grid_x=8,
    grid_y=8
)

# -------- Load Face Cascade -------- #
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# -------- Function to get Images & Labels -------- #
def getImagesAndLabels(path):
    faceSamples = []
    ids = []

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    for imagePath in imagePaths:
        try:
            # Convert image to grayscale
            pilImage = Image.open(imagePath).convert('L')
            img_numpy = np.array(pilImage, 'uint8')

            # Extract ID from filename
            # Format: User.ID.Count.jpg
            filename = os.path.split(imagePath)[-1]
            id = int(filename.split(".")[1])

            faces = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)

        except Exception as e:
            print(f"[WARNING] Skipping file: {imagePath}")
            continue

    return faceSamples, ids

# -------- Training -------- #
print("[INFO] Training faces... Please wait")

faces, ids = getImagesAndLabels(dataset_path)

if len(faces) == 0:
    print("[ERROR] No faces found. Please register users first.")
    exit()

recognizer.train(faces, np.array(ids))

# -------- Save Model -------- #
if not os.path.exists('trainer'):
    os.makedirs('trainer')

recognizer.write('trainer/trainer.yml')

print(f"[INFO] Training completed. {len(set(ids))} users trained.")
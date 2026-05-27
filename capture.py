import cv2

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Camera failed ❌")
    exit()

print("Camera started ✅")

while True:
    ret, img = cam.read()

    if not ret:
        print("Frame error ❌")
        break

    cv2.imshow("Test", img)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
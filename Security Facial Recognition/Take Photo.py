import cv2

cam = cv2.VideoCapture(-1)
cv2.namedWindow("test")
img_counter = 0
running = True

while running:
    ret, frame = cam.read()
    if ret:
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            running = False
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
    else:
        running = False

cam.release()
cv2.destroyAllWindows()
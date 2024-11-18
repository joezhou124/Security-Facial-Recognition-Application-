import face_recognition
import cv2
import numpy as np
import pyautogui
from selenium import webdriver
import time
import os


class FaceRecognitionSecurity:
    def __init__(self):
        # Authentication credentials
        self.gmail = "ENTER GMAIL HERE"
        self.password = "ENTER PASSWORD HERE"

        # Initialize video capture
        self.video_capture = cv2.VideoCapture(0)

        # Load and encode known face
        root_image = face_recognition.load_image_file("YOUR PHOTO PATH")
        root_encoding = face_recognition.face_encodings(root_image)[0]

        # Known faces database
        self.known_face_encodings = [root_encoding]
        self.known_face_names = ["YOUR NAME"]

    def process_frame(self, frame):
        """Process a single frame and return name of detected person"""
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        name = "Unknown"

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            self.draw_face_box(frame, left, top, right, bottom, name)

        return name

    def draw_face_box(self, frame, left, top, right, bottom, name):
        """Draw rectangle and name around detected face"""
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    def trigger_security_action(self):
        """Handle unauthorized access"""
        driver = webdriver.Chrome(executable_path="CHROME DRIVER PATH")
        driver.get("https://www.google.com/android/find")
        time.sleep(2)

        # Login sequence
        pyautogui.typewrite(self.gmail)
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.typewrite(self.password)
        pyautogui.press("enter")
        time.sleep(5)

        # Navigation sequence
        pyautogui.click(x=85, y=231)
        time.sleep(2)
        pyautogui.click(x=200, y=495)
        pyautogui.hotkey('ctrlleft', 'altleft', 'l')

    def handle_authorized_access(self):
        """Handle authorized access"""
        print("Welcome BOSS")
        os.system("gnome-terminal")

    def run(self):
        """Main loop to run the security system"""
        try:
            while True:
                ret, frame = self.video_capture.read()
                if not ret:
                    break

                name = self.process_frame(frame)

                # Handle security actions based on recognition
                if name != "YOUR NAME":
                    self.trigger_security_action()
                else:
                    self.handle_authorized_access()

                # Display the resulting image
                cv2.imshow('Video', frame)

                # Break loop on 'q' press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            # Cleanup
            self.video_capture.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    security_system = FaceRecognitionSecurity()
    security_system.run()
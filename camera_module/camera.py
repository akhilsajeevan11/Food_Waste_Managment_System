import cv2
import os
import time

class Camera:
    def __init__(self, index):
        self.index = index
        self.camera = None

    def initialize(self):
        self.camera = cv2.VideoCapture(self.index)
        if not self.camera.isOpened():
            print("Error: Camera not accessible.")
            exit(1)

    def capture_image(self, save_folder):
        """Capture an image from the camera and save it."""
        print("Capturing Image")
        time.sleep(2)  # Allow time for camera to adjust
        ret, frame = self.camera.read()
        if ret:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_folder, f"image_{timestamp}.jpg")
            try:
                cv2.imwrite(filename, frame)
                print(f"Image captured and saved as {filename}")
                return filename  # Return the filename if successful
            except Exception as e:
                print(f"Error saving image: {e}")
                return None
        else:
            print("Error: Could not capture image.")
            return None
        
    def release(self):
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()

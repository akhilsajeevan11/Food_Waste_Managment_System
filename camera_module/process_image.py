from camera_module.camera import Camera
from setup.setup import load_config

# Load configuration
config = load_config()
baud_rate = config['baud_rate']

camera_index=config['camera_index']
image_directory=config['image_directory']




def capture_image():
    try:
        print("STARTING CAMERA MODULE")

        # Initialize the camera object
        camera = Camera(camera_index)
        camera.initialize()

        filename = camera.capture_image(image_directory)
       

    except Exception as e:
        print(f"Failed to capture image: {e}")

    finally:
        # Ensure the camera is properly released
        camera.release()
        print("Camera module released")

    return filename
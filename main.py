
import os
import time
import socket
import threading
from datetime import datetime
from serial_communcation.read_arduino_serial import ArduinoSerial
from setup.setup import load_config,ensure_directory_exists
from process_module.process_data import process_data
from detection_engine.food_model.food_model_inference import load_food_model

# Load configuration
config = load_config()
arduino_port = config['arduino_port']
baud_rate = config['baud_rate']
image_directory=config['image_directory']



# Ensure the capture_images directory exists
ensure_directory_exists(image_directory)

def main():

   
    arduino = ArduinoSerial(arduino_port, baud_rate)
    arduino.connect()
    arduino.send_signal("START\n")
    print("Starting Application :Reset Sensor: Arduino")
    
    while True:
        signal = arduino.read_signal()
        

        if signal and "OBJECT_DETECTED" in signal:
            distance = signal.split(": ")[1] 
            print(f"OBJECT DETECTED in {distance}cm")

            process_data()
    
            # # Send "START" command to Arduino to reactivate the sensor
            arduino.send_signal("START\n")
            print("Reset Sensor: Arduino")

            #insert into database
             # Start background thread for database insertion
            # threading.Thread(target).start()
        else:
            
            print("Waiting for object detection...")

        time.sleep(1)  # Sleep for a second before checking again


    arduino.close()

if __name__ == '__main__':



    main()
    
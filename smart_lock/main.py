import RPi.GPIO as GPIO
import time
import threading
from camera import Camera
from pir_sensor import PIRSensor
from keypad import Keypad
from api.app import app as flask_app

# Set the GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
PIR_PIN = 18

# Create instances of the Camera, PIRSensor, and Keypad classes
camera = Camera()
pir_sensor = PIRSensor(PIR_PIN)
keypad = Keypad()

# Function to monitor the PIR sensor in a separate thread
def monitor_pir(pir, camera):
    while True:
        if pir.detect_motion():
            camera.activate()
        #else:
            #camera.deactivate()
        time.sleep(0.1)  # Adjust the sleep duration as needed

# Function to monitor the Keypad in a separate thread
def monitor_keypad(keypad):
    while True:
        keypad.usage()
        time.sleep(0.1)  # Adjust the sleep duration as needed

try:
    print("PIR sensor initialized. Monitoring for motion detection and keypad input...")
    
    # Create threads for monitoring PIR and Keypad simultaneously
    pir_thread = threading.Thread(target=monitor_pir, args=(pir_sensor, camera))
    keypad_thread = threading.Thread(target=monitor_keypad, args=(keypad,))
    flask_thread = threading.Thread(target=flask_app.run, kwargs={'host': '0.0.0.0', 'use_reloader': False})

    
    pir_thread.start()  # Start the thread to monitor the PIR sensor
    keypad_thread.start()  # Start the thread to monitor the keypad
    flask_thread.start()  # Start the Flask app thread
    
    pir_thread.join()
    keypad_thread.join()
    flask_thread.join()

except KeyboardInterrupt:
    #door.close()  # Example: Close the door
    cam.deactivate()  # Example: Deactivate the camera
    GPIO.cleanup()
    print("Exiting...")
    sys.exit(0)
    

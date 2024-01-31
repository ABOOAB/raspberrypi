# pir_sensor.py
import RPi.GPIO as GPIO

class PIRSensor:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def detect_motion(self):
        return GPIO.input(self.pin)
        

"""GPIO.setmode(GPIO.BCM)
pir = PIRSensor(18)
while True:
    if pir.detect_motion():
        print("1")
    else :
        print('0')"""


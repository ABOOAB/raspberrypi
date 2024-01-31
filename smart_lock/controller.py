import serial
import time

class Door: 
    unlock = False
    opening_time = 5
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)

    def cmd(self, message):
        self.ser.write(message.encode())

    def open(self):
        self.cmd('1')
        self.unlock = True
        print("Door is open .")
        start_time = time.time()
        while time.time() - start_time <= self.opening_time:
            continue
        self.close()

    def close(self):
        if self.unlock:
            self.cmd('0')
            self.unlock = False
            print("Door is closing....")



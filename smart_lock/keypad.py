# this is my code 

from time import sleep
import RPi.GPIO as GPIO
from controller import Door

door = Door()

class Keypad:
    pw = '1234'
    reset_pw = 'C' + pw + 'C'
    reset = '##*#'
    max_attempts = 3
    attempt_count = 0

    def __init__(self,Enter = 'D', rows=[17, 27, 22, 5], columns = [6, 13, 19, 26],
                 key_labels = [['1', '2', '3', 'A'],
                               ['4', '5', '6', 'B'],
                               ['7', '8', '9', 'C'],
                               ['*', '0', '#', 'D']],
                 ):

        self.rows = rows
        self.columns = columns
        self.Enter = Enter
        self.key_labels = key_labels
        GPIO.setmode(GPIO.BCM)
        for i in rows:
            GPIO.setup(i, GPIO.OUT)
        for j in columns:
            GPIO.setup(j, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def read_keypad(self):
        key_strokes=''
        pressed = False
        old_pressed = False
        while True:
            pressed = False
            for row in range(4):
                for col in range(4):
                    GPIO.output(self.rows[row], GPIO.HIGH)
                    button_val = GPIO.input(self.columns[col])
                    GPIO.output(self.rows[row], GPIO.LOW)
                    if button_val:
                        my_char = self.key_labels[row][col]
                        if my_char == self.Enter :
                            return key_strokes
                        pressed = True
                        if pressed and not old_pressed:
                            key_strokes = key_strokes +  my_char
            old_pressed = pressed
            sleep(0.25)


    def pw_change(self):
        print("Enter new password")
        sleep(0.2)
        self.pw = self.read_keypad()
        print("your password has been changed correctly to : ", end='')
        print(self.pw)

    def usage(self):
        
        my_string = self.read_keypad()
        if my_string == self.pw:
                door.open()
                self.restart()
                sleep(0.2)


        elif my_string == self.reset_pw:
            self.pw_change()
            self.restart()
            sleep(0.2)

        elif my_string == self.reset:
            self.pw = '1234'
            print("keypad has been reseted ..")
            sleep(0.2) 

        else:
            print("Incorrect password. Try again.")
            self.attempt_count += 1
            if self.attempt_count >= self.max_attempts:
                # send the photo of the offender to the owner 
                print("Offender...")
                sleep(0.2)
                self.restart()
                sleep(0.2)

    def restart(self):
        self.attempt_count = 0
        print("keypad has been restarted. ")

if __name__ == "__main__":
    keypad = Keypad()

    while True:
        keypad.usage()
        sleep(0.2)

    GPIO.cleanup()

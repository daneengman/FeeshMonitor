import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(5, GPIO.OUT)

GPIO.output(5, 0)

time.sleep(1)
GPIO.output(5, 1)
time.sleep(1)
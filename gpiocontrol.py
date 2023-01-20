import RPi.GPIO as GPIO
import time

white = 5
blue = 6

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(white, GPIO.OUT)
# GPIO.setup(blue, GPIO.OUT)

#sets both pins to high for a moment, then back to low
GPIO.output(white, GPIO.HIGH)
# GPIO.output(blue, GPIO.HIGH)
input("proceed to low\n")
GPIO.output(white, GPIO.LOW)
# GPIO.output(blue, GPIO.LOW)
input("exit\n")

GPIO.cleanup()
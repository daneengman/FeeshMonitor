import RPi.GPIO as GPIO
import time

white = 5
blue = 6

GPIO.setmode(GPIO.BOARD)
GPIO.setup(white, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

#sets both pins to high for a moment, then back to low
GPIO.output(white, GPIO.HIGH)
GPIO.output(blue, GPIO.HIGH)
time.sleep(0.2)
GPIO.output(white, GPIO.LOW)
GPIO.output(blue, GPIO.LOW)

GPIO.cleanup()
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press a button! (Ctrl+C) for terminating.")

try:
    while True:
        if GPIO.input(26) == GPIO.LOW:
            print("Button 1")
            time.sleep(0.3)
        if GPIO.input(16) == GPIO.LOW:
            print("Button 2")
            time.sleep(0.3)
        if GPIO.input(26) == GPIO.LOW:
            print("Button 3")
            time.sleep(0.3)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("End.")
    
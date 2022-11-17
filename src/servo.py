import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12,GPIO.OUT)

servo = GPIO.PWM(12,50)

servo.start(0)
print("waiting for 1 second")
time.sleep(1)

print("rotating at intervals of 12 degrees")
duty = 2
while duty<=12:
    servo.ChangeDutyCycle(duty)
    time.sleep(1)
    duty=duty+1

print("turning back to 0 degrees")
servo.ChangeDutyCycle(2)
time.sleep(1)
servo.ChangeDutyCycle(0)

servo.stop()
GPIO.cleanup()
print("eveything cleaned up")
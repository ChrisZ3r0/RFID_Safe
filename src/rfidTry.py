import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    id, text = reader.read()
    print(f"Id: {id}, text: {text}")
finally:
    GPIO.cleanup()

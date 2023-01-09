#!/usr/bin/env python

import os
import time
from dotenv import load_dotenv
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from picamera2 import Picamera2
from features.sendEmailUponLogin import EmailSender
from features.getDate import getDateAndTimeFormatted
from features.PiGpio import PiGpio
from features.Safe import Safe
from features.Logger import Logger
from features.Plotter import Plotter
from features.Camera import Camera


def main():
    load_dotenv()

    PiGpio.setGpioModeToBoard()
    gpio = PiGpio()
    gpio.setupGpio()
    GPIO.setup(12, GPIO.OUT)
    servo = GPIO.PWM(12, 50)
    servo.start(0)
    safe = Safe()
    email = EmailSender(os.getenv("GMAIL_SENDER_ADDRESS"), os.getenv("GMAIL_APP_CODE"), os.getenv("GMAIL_SENDER_ADDRESS"))
    rfidReader = SimpleMFRC522() # Ennek nem lehetne PIN-t adni? Mert ha nem adsz, defaultra megy, és megtalálja, de itt nem?
    logger = Logger()
    plotter = Plotter()
    camera = Camera(Picamera2())
    camera.startPreview()
    try:
        inputPin = ""
        while True:
            characterGot = gpio.readNumpadInput()
            inputPin += characterGot
            print(inputPin)
            if characterGot and len(inputPin) == 4:
                loginTime = getDateAndTimeFormatted()

                camera.captureImage(loginTime)
                if inputPin == safe.admin_mode:
                    print("Touch your RFID")
                    cardId, text = rfidReader.read()
                    print(text)
                    if text == safe.admin_password:
                        print("Admin login")
                        logger.logAttemptedLogin(loginTime, 1)
                        duty = 8  # 8n a nyilt 14-15 aa zart
                        while duty <= 15:  # 90 / 6 degree => 15 rotations
                            servo.ChangeDutyCycle(duty)
                            time.sleep(1)
                            duty = duty + 1
                        email.setUpAlertEmailForAdminLogin(loginTime)
                        email.sendAnAlertEmail()
                    else:
                        gpio.startBuzzer()
                        gpio.stopBuzzer()

                elif safe.pinIsValid(inputPin):
                    print("Pin is valid")
                    logger.logAttemptedLogin(loginTime, 1)

                    duty = 8   # 8n a nyilt 14-15 aa zart
                    while duty <= 15:  # 90 / 6 degree => 15 rotations
                        servo.ChangeDutyCycle(duty)
                        time.sleep(1)
                        duty = duty + 1

                    email.setUpAlertEmailForValidLogin(loginTime)
                    email.sendAnAlertEmail()
                    for i in range(3):
                        print(f"Starting {i}")
                        gpio.startBuzzer()
                        gpio.startLed(0.1)
                        print(f"Stopping {i}")
                        gpio.stopBuzzer()
                        gpio.stopLed(0.1)

                    gpio.startBuzzer()
                    gpio.startLed(0)
                    time.sleep(0.5)
                    gpio.stopBuzzer()
                    gpio.stopLed(0)

                elif inputPin == safe.plotter_mode:
                    plotter.evaluateLoginData()
                    plotter.createAndSaveDiagram(loginTime)
                    email.setUpAlertEmailForPlotter(loginTime)
                    email.sendAnAlertEmail()

                else:
                    print("Pin is not valid")
                    gpio.startBuzzer()
                    time.sleep(0.5)
                    gpio.stopBuzzer()
                    logger.logAttemptedLogin(loginTime, 0)
                    servo.ChangeDutyCycle(0)
                    email.setUpAlertEmailForNotValidLogin(loginTime)
                    email.sendAnAlertEmail()
                    gpio.startLed(0)
                    gpio.stopLed(0)
                inputPin = ""

            else:
                time.sleep(0.1)
            if characterGot:
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nApplication stopped!")
    finally:
        servo.stop()
        gpio.gpioCleanup()


if __name__ == "__main__":
    main()

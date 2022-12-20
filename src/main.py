#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from picamera2 import Picamera2
import time
from features.sendEmailUponLogin import EmailSender
from features.getDate import getDateAndTimeFormatted
from features.PiGpio import PiGpio
from features.Safe import Safe
from features.Logger import Logger
from features.Plotter import Plotter
from features.Camera import Camera


def main():
    PiGpio.setGpioModeToBoard()
    gpio = PiGpio()
    gpio.setupGpio()
    GPIO.setup(12, GPIO.OUT)
    servo = GPIO.PWM(12, 50)
    servo.start(0)
    safe = Safe()
    email = EmailSender("toreky.zsombor@gmail.com", "", "tore.plays01@gmail.com")
    rfidReader = SimpleMFRC522()
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
                        duty = 1
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
                    duty = 1
                    while duty <= 15:  # 90 / 6 degree => 15 rotations
                        servo.ChangeDutyCycle(duty)
                        time.sleep(1)
                        duty = duty + 1
                    email.setUpAlertEmailForValidLogin(loginTime)
                    email.sendAnAlertEmail()
                    for i in range(1, 4):
                        gpio.startBuzzer()
                        gpio.startLed(1)
                        gpio.stopBuzzer()
                        gpio.stopLed(1)

                elif inputPin == safe.plotter_mode:
                    plotter.evaluateLoginData()
                    # plotter.createAndShowDiagram()

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

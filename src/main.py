#!/usr/bin/env python

import os
import time
import pigpio
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

    servo = 18
    pwm = pigpio.pi()
    pwm.set_mode(servo, pigpio.OUTPUT)
    pwm.set_PWM_frequency(servo, 50)
    GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
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
                gpio.startBuzzer()
                time.sleep(0.5)
                gpio.stopBuzzer()
                loginTime = getDateAndTimeFormatted()

                camera.captureImage(loginTime)
                if inputPin == safe.admin_mode:
                    print("Touch your RFID")
                    cardId, text = rfidReader.read()
                    print(text)
                    if cardId ==safe.admin_password: #changed to the card id, it is unique so it should be safe
                        print("Admin login")
                        logger.logAttemptedLogin(loginTime, 1)
                        print( "90 deg" )
                        pwm.set_servo_pulsewidth( servo, 1500 ) ;
                        # time.sleep( 10 )
                        print("opening servo")
                        while GPIO.input(32) == GPIO.LOW:
                            print("in while loop")
                            time.sleep(0.5)
                            print("while loop after sleep")
                        print("after while")
                        print( "0 deg" )
                        pwm.set_servo_pulsewidth( servo, 500 ) ;
                        email.setUpAlertEmailForAdminLogin(loginTime)
                        email.sendAnAlertEmail()
                    else:
                        logger.logAttemptedLogin(loginTime, 0)
                        email.setUpAlertEmailForNotValidLogin(loginTime)
                        email.sendAnAlertEmail()
                        gpio.startBuzzer()
                        time.sleep(0.5)
                        gpio.stopBuzzer()
                        gpio.startLed(0)
                        gpio.stopLed(0)

                elif safe.pinIsValid(inputPin):
                    print("Pin is valid")
                    logger.logAttemptedLogin(loginTime, 1)

                    print( "90 deg" )
                    pwm.set_servo_pulsewidth( servo, 1500 ) ;
                    # time.sleep( 10 )
                    print("opening servo")
                    while GPIO.input(32) == GPIO.LOW:
                        print("in while loop")
                        time.sleep(0.5)
                        print("while loop after sleep")
                    print("after while")
                    print( "0 deg" )
                    pwm.set_servo_pulsewidth( servo, 500 ) ;
                    
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
                    gpio.startLed(0.1)
                    time.sleep(0.5)
                    gpio.stopBuzzer()
                    gpio.stopLed(0.1)

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
                    email.setUpAlertEmailForNotValidLogin(loginTime)
                    email.setUpAlertEmailForImage(loginTime)
                    email.sendAnAlertEmail()
                    gpio.startLed(0)
                    gpio.stopLed(0)
                inputPin = ""

            else:
                time.sleep(0.1)
            if characterGot:
                gpio.startBuzzer()
                time.sleep(0.5)
                gpio.stopBuzzer()
    except KeyboardInterrupt:
        print("\nApplication stopped!")
    finally:
        pwm.set_PWM_dutycycle( servo, 0 )
        pwm.set_PWM_frequency( servo, 0 )
        gpio.gpioCleanup()

if __name__ == "__main__":
    main()

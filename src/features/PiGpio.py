import RPi.GPIO as GPIO
from gpiozero import Buzzer, LED
from mfrc522 import SimpleMFRC522
import time


class PiGpio:
    def __init__(self, servo):
        self.L4 = 37
        self.L2 = 33
        self.L3 = 35
        self.L1 = 31
        self.C1 = 32
        self.C2 = 36
        self.C3 = 38
        self.C4 = 40
        self.led = ? # Led PIN-je
        self.buzzer = Buzzer(16)
        self.servo = servo

    def setupGpio(self):
        GPIO.setwarnings(False)
        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)
        GPIO.setup(self.L3, GPIO.OUT)
        GPIO.setup(self.L4, GPIO.OUT)
        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.led, GPIO.OUT)

    def startServo(self):
        self.servo.start(0)

    def stopServo(self):
        self.servo.stop()

    def setNeutralState(self):
        self.servo.ChangeDutyCycle(0)

    def setHighState(self):
        duty = 0
        while duty <= 15:  # 90 / 6 degree => 15 rotations
            self.servo.ChangeDutyCycle(duty)
            time.sleep(1)
            duty = duty + 1

    def startBuzzer(self):
        self.buzzer.on()
        time.sleep(0.5)

    def stopBuzzer(self):
        self.buzzer.off()

    def startLed(self):
        GPIO.output(self.led, GPIO.HIGH)
        print("LED on")
        time.sleep(1)

    def stopLed(self):
        GPIO.output(self.led, GPIO.LOW)
        print("LED off")

    @staticmethod
    def setGpioModeToBoard():
        GPIO.setmode(GPIO.BOARD)

    @staticmethod
    def setGpioModeToBcm():
        GPIO.setmode(GPIO.BCM)

    def readNumpadInput(self):
        character = self.readLine(self.L1, ["1", "2", "3", "A"])
        if not character:
            character = self.readLine(self.L2, ["4", "5", "6", "B"])
        if not character:
            character = self.readLine(self.L3, ["7", "8", "9", "C"])
        if not character:
            character = self.readLine(self.L4, ["*", "0", "#", "D"])
        return character

    def readLine(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if GPIO.input(self.C1):
            return characters[0]
        if GPIO.input(self.C2):
            return characters[1]
        if GPIO.input(self.C3):
            return characters[2]
        if GPIO.input(self.C4):
            return characters[3]
        GPIO.output(line, GPIO.LOW)

        return ""

    @staticmethod
    def gpioCleanup():
        GPIO.cleanup()

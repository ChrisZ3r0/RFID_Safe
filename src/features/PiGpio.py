import RPi.GPIO as GPIO
from gpiozero import Buzzer
from mfrc522 import SimpleMFRC522
import time


class PiGpio:
    def __init__(self, servo): # servo -> GPIO.PWM(12, 50) 12 helyett is másik
        self.L1 = 25
        self.L2 = 8
        self.L3 = 7
        self.L4 = 1
        self.C1 = 12
        self.C2 = 16
        self.C3 = 20
        self.C4 = 21
        self.buzzer = Buzzer(23)
        self.servo = servo

    def setupGpio(self):
        GPIO.setwarnings(False)
        # GPIO.setup(12, GPIO.OUT) --> Itt a 12-es helyett másikra kell tenni
        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)
        GPIO.setup(self.L3, GPIO.OUT)
        GPIO.setup(self.L4, GPIO.OUT)
        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def startServo(self):
        self.servo.start(0)

    def stopServo(self):
        self.servo.stop()

    def setNeutralState(self):
        self.setGpioModeToBoard()
        self.servo.ChangeDutyCycle(0)

    def setHighState(self):
        self.setGpioModeToBoard()
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
        time.sleep(0.5)

    @staticmethod
    def setGpioModeToBoard():
        GPIO.setmode(GPIO.BOARD)

    @staticmethod
    def setGpioModeToBcm():
        GPIO.setmode(GPIO.BCM)

    # noinspection PyTypeChecker
    def readNumpadInput(self):
        character = self.readLine(self.L1, ["1", "2", "3", "A"])
        if not character:
            character = self.readLine(self.L2, ["4", "5", "6", "B"])
        if not character:
            character = self.readLine(self.L3, ["7", "8", "9", "C"])
        if not character:
            character = self.readLine(self.L4, ["*", "0", "#", "D"])
        return character

    @staticmethod
    def readLine(line, characters):
        GPIO.output(line, GPIO.HIGH)
        if GPIO.input(line.C1):
            return characters[0]
        if GPIO.input(line.C2):
            return characters[1]
        if GPIO.input(line.C3):
            return characters[2]
        if GPIO.input(line.C4):
            return characters[3]
        GPIO.output(line, GPIO.LOW)

        return ""

    @staticmethod
    def gpioCleanup():
        GPIO.cleanup()

import RPi.GPIO as GPIO
import time


class PiGpio:
    def __init__(self):
        self.L4 = 37
        self.L2 = 33
        self.L3 = 35
        self.L1 = 31
        self.C1 = 32
        self.C2 = 36
        self.C3 = 38
        self.C4 = 40
        self.greenLed = 18 # Led PIN-je
        self.redLed = 11
        self.buzzer = 16

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
        GPIO.setup(self.buzzer, GPIO.OUT)
        GPIO.setup(self.greenLed, GPIO.OUT)
        GPIO.setup(self.redLed, GPIO.OUT)

    def startBuzzer(self):
        GPIO.output(self.buzzer, GPIO.HIGH)

    def stopBuzzer(self):
        GPIO.output(self.buzzer, GPIO.LOW)
        time.sleep(0.1)

    def startLed(self, isGreen):
        if isGreen:
            GPIO.output(self.greenLed, GPIO.HIGH)
        else:
            GPIO.output(self.redLed, GPIO.HIGH)
        time.sleep(0.1)

    def stopLed(self, isGreen):
        if isGreen:
            GPIO.output(self.greenLed, GPIO.LOW)
        else:
            GPIO.output(self.redLed, GPIO.LOW)
        time.sleep(0.1)

    @staticmethod
    def setGpioModeToBoard():
        GPIO.setmode(GPIO.BOARD)

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

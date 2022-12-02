import RPi.GPIO as GPIO
import time
from features.sendEmailUponLogin import sendAnAlertEmail
from features.getDate import getDateAndTimeFormatted


class PiGpio:
    def __init__(self, servo): # servo -> GPIO.PWM(12, 50)
        self.L1 = 25
        self.L2 = 8
        self.L3 = 7
        self.L4 = 1
        self.C1 = 12
        self.C2 = 16
        self.C3 = 20
        self.C4 = 21
        self.servo = servo

    def setupGpio(self):
        GPIO.setwarnings(False)
        # GPIO.setup(12, GPIO.OUT) --> Itt a 12-es az nem a C1-é?
        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)
        GPIO.setup(self.L3, GPIO.OUT)
        GPIO.setup(self.L4, GPIO.OUT)
        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    @staticmethod
    def setGpioModeToBoard():
        GPIO.setmode(GPIO.BOARD)

    @staticmethod
    def setGpioModeToBcm():
        GPIO.setmode(GPIO.BCM)

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

    def startServo(self):
        self.servo.start(0)

    def stopServo(self):
        self.servo.stop()

    @staticmethod
    def gpioCleanup():
        GPIO.cleanup()

    def setNeutralState(self):
        self.servo.ChangeDutyCycle(0)

    def setHighState(self):
        duty = 0
        while duty <= 15:  # 90 / 6 degree => 15 rotations
            self.servo.ChangeDutyCycle(duty)
            time.sleep(1)
            duty = duty + 1


class Safe:
    def __init__(self):
        self.isOpen = False

    def getIsOpen(self) -> bool:
        return self.isOpen

    def setIsOpen(self, isOpen : bool):
        self.isOpen = isOpen

    @staticmethod
    def setPassword(password : str):
        # Opening it in writing mode already wipes it clear
        with open("/home/chris/RFID_Safe/src/password/pwd.txt", "w") as f:
            f.write(password)

    @staticmethod
    def getPassword():
        with open("/home/chris/RFID_Safe/src/password/pwd.txt", "r") as f:
            password = f.readline()
        return password

    @staticmethod
    def pinIsValid(pin : str):
        with open("/home/chris/RFID_Safe/src/password/pwd.txt", "r") as f:
            password = f.readline()
        return password == pin


# noinspection PyTypeChecker
def main():
    gpio = PiGpio(GPIO.PWM(12, 50))
    safe = Safe()
    try:
        inputPin = ""
        while True:
            characterGot = ""

            gpio.setGpioModeToBcm()
            characterGot = gpio.readLine(gpio.L1, ["1", "2", "3", "A"])
            if not characterGot:
                characterGot = gpio.readLine(gpio.L2, ["4", "5", "6", "B"])
            if not characterGot:
                characterGot = gpio.readLine(gpio.L3, ["7", "8", "9", "C"])
            if not characterGot:
                characterGot = gpio.readLine(gpio.L4, ["*", "0", "#", "D"])

            inputPin += characterGot
            if characterGot and len(inputPin) == 4:
                if safe.pinIsValid(inputPin):
                    print("Pin is valid")
                    gpio.setGpioModeToBoard()
                    gpio.setHighState()
                    # sendAnAlertEmail(getDateAndTimeFormatted(), True)
                    inputPin = ""
                else:
                    print("Pin is not valid")
                    gpio.setGpioModeToBoard()
                    gpio.setNeutralState()
                    # sendAnAlertEmail(getDateAndTimeFormatted(), False)
                    inputPin = ""
            else:
                time.sleep(0.1)
            if characterGot:
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nApplication stopped!")


if __name__ == "__main__":
    main()

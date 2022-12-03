import RPi.GPIO as GPIO
from gpiozero import Buzzer
from mfrc522 import SimpleMFRC522
import time
from features.sendEmailUponLogin import EmailSender
from features.getDate import getDateAndTimeFormatted


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


class Rfid:
    def __init__(self, reader):
        self.reader = reader

    def readId(self):
        return self.reader.read()[0]

    def readText(self):
        return self.reader.read()[1]

    def setText(self, text):
        self.reader.write(text)


class Safe:
    def __init__(self):
        self.isOpen = False
        self.admin_mode = "AAAA"
        self.admin_password = "0000"

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


class Logger:
    def __init__(self, path="/home/chris/RFID_Safe/src/login/login.csv"):
        self.path = path

    def logAttemptedLogin(self, timeOfLogin, valid : int):
        with open(self.path, "a") as f:
            f.write(timeOfLogin + "," + str(valid) + "\n")


def main():
    gpio = PiGpio(GPIO.PWM(12, 50)) # 12  -> ??
    safe = Safe()
    email = EmailSender("myEmail@gmail.com", "myPassword", "targetEmail@gamil.com", "My Name")
    rfid = Rfid(SimpleMFRC522())
    logger = Logger()
    try:
        inputPin = ""
        while True:
            characterGot = ""

            gpio.setGpioModeToBcm()
            characterGot = gpio.readNumpadInput()

            inputPin += characterGot
            if characterGot and len(inputPin) == 4:
                loginTime = getDateAndTimeFormatted()
                if inputPin == safe.admin_mode:
                    print("Touch your RFID")
                    if rfid.readText() == safe.admin_password:
                        print("Admin login")
                        logger.logAttemptedLogin(loginTime, 1)
                        gpio.setHighState()
                        email.setUpAlertEmailForAdminLogin(loginTime)
                        # email.sendAnAlertEmail()
                    else:
                        gpio.startBuzzer()
                        gpio.stopBuzzer()
                elif safe.pinIsValid(inputPin):
                    print("Pin is valid")
                    logger.logAttemptedLogin(loginTime, 1)
                    gpio.setHighState()
                    email.setUpAlertEmailForValidLogin(loginTime)
                    # email.sendAnAlertEmail()
                else:
                    print("Pin is not valid")
                    gpio.startBuzzer()
                    gpio.stopBuzzer()
                    logger.logAttemptedLogin(loginTime, 0)
                    gpio.setNeutralState()
                    email.setUpAlertEmailForNotValidLogin(loginTime)
                    # email.sendAnAlertEmail()
                inputPin = ""
            else:
                time.sleep(0.1)
            if characterGot:
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nApplication stopped!")
    finally:
        gpio.gpioCleanup()


if __name__ == "__main__":
    main()

class Safe:
    def __init__(self):
        self.isOpen = False
        self.admin_mode = "AAAA"
        self.admin_password = "0000"
        self.plotter_mode = "BBBB"

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
        print("Reading in")
        with open("/home/chris/RFID_Safe/src/password/pwd.txt", "r") as f:
            password = f.readline()
        return password == pin

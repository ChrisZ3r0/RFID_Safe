class Logger:
    def __init__(self, path="/home/chris/RFID_Safe/src/login/login.csv"):
        self.path = path

    def logAttemptedLogin(self, timeOfLogin, valid : int):
        with open(self.path, "a") as f:
            f.write(timeOfLogin + "," + str(valid) + "\n")

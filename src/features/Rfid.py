class Rfid:
    def __init__(self, reader):
        self.reader = reader

    def readId(self):
        return self.reader.read()[0]

    def readText(self):
        return self.reader.read()[1]

    def setText(self, text):
        self.reader.write(text)
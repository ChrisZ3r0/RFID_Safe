class Rfid:
    def __init__(self, reader):
        self.reader = reader

    def read(self):
        return self.reader.read()

    def setText(self, text):
        self.reader.write(text)

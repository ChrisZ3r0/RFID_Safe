class Rfid:
    def __init__(self, reader):
        self.reader = reader

    def read(self):
        cardId, text = self.reader.read()
        return cardId, text

    def setText(self, text):
        self.reader.write(text)

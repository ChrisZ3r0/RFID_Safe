import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self, path="/home/chris/RFID_Safe/src/login/login.csv"):
        self.path = path
        self.monthsLabels = []
        self.validLogins = []
        self.inValidLogins = []

    def evaluateLoginData(self):
        with open(self.path, "r") as file:
            validCounter = 0
            inValidCounter = 0
            for line in file.readlines():
                yearAndMonth = line.strip().split(",")[0].split("_")[0].split("-")[:2]
                if len(self.monthsLabels) != 0 and yearAndMonth not in self.monthsLabels:
                    self.validLogins.append(validCounter)
                    self.inValidLogins.append(inValidCounter)
                    validCounter = 0
                    inValidCounter = 0
                valid = line.strip().split(",")[1]
                if int(valid):
                    validCounter += 1
                else:
                    inValidCounter += 1
                if yearAndMonth not in self.monthsLabels:
                    self.monthsLabels.append(yearAndMonth)

            self.validLogins.append(validCounter)
            self.inValidLogins.append(inValidCounter)
        self.formatLabels()

    def formatLabels(self):
        for i, label in enumerate(self.monthsLabels.copy()):
            self.monthsLabels.append(label[0] + ", " + label[1])

    def createAndShowDiagram(self):
        x = np.arange(len(self.monthsLabels))  # the label locations
        width = 0.2  # the width of the bars
        fig, ax = plt.subplots()
        rectangle1 = ax.bar(x - width / 2, self.validLogins, width, label='Valid Logins')
        rectangle2 = ax.bar(x + width / 2, self.inValidLogins, width, label='Invalid Logins')
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Attempted Logins')
        ax.set_title('Safe Login Visualization')
        ax.set_xticks(x, self.monthsLabels)
        ax.legend()
        ax.bar_label(rectangle1, padding=3)
        ax.bar_label(rectangle2, padding=3)
        fig.tight_layout()
        plt.show()
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
            self.monthsLabels = []
            self.validLogins = []
            self.inValidLogins = []
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
        self._formatLabels()

    def _formatLabels(self):
        for i, label in enumerate(self.monthsLabels.copy()):
            self.monthsLabels[i] = label[0] + ", " + label[1]

    def createAndSaveDiagram(self, timeOfSaving):
        x = np.arange(len(self.monthsLabels))
        width = 0.2
        fig, ax = plt.subplots()
        ax.set_ylabel("Attempted Logins")
        ax.set_title("Safe Login Visualization")
        ax.set_xticks(x, self.monthsLabels)
        ax.legend()
        for i in range(len(self.monthsLabels)):
            plt.text(i, self.validLogins[i], self.validLogins[i], ha="center", va="bottom")
            plt.text(i, self.inValidLogins[i], self.inValidLogins[i], ha="center", va="bottom")
        fig.tight_layout()

        plt.savefig(f"/home/chris/RFID_Safe/src/diagrams/{timeOfSaving}.png")

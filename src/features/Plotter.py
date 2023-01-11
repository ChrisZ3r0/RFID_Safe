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
        width = 0.35
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, self.validLogins, width, label="Valid Logins")
        rects2 = ax.bar(x + width/2, self.inValidLogins, width, label="Invalid Logins")

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel("Attempted Logins")
        ax.set_title("Safe Login Visualization")
        ax.set_xticks(x)
        ax.set_xticklabels(self.monthsLabels)
        ax.legend()

        self.autolabel(ax, rects1)
        self.autolabel(ax, rects2) #wrote ax first argument

        fig.tight_layout()
        plt.savefig(f"/home/chris/RFID_Safe/src/diagrams/{timeOfSaving}.png")

    def autolabel(self, ax, rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom')

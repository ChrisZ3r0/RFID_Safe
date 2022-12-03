import matplotlib.pyplot as plt
import numpy as np

monthsLabels = []
validLogins = []
inValidLogins = []

with open("C:/Users/torek/PycharmProjects/RFID_Safe/src/login/login.csv", "r") as file:
	validCounter = 0
	inValidCounter = 0
	for line in file.readlines():
		yearAndMonth = line.strip().split(",")[0].split("_")[0].split("-")[:2]
		if len(monthsLabels) != 0 and yearAndMonth not in monthsLabels:
			validLogins.append(validCounter)
			inValidLogins.append(inValidCounter)
			validCounter = 0
			inValidCounter = 0
		valid = line.strip().split(",")[1]
		if int(valid):
			validCounter += 1
		else:
			inValidCounter += 1
		if yearAndMonth not in monthsLabels:
			monthsLabels.append(yearAndMonth)

	validLogins.append(validCounter)
	inValidLogins.append(inValidCounter)

# Cleaning up
for i, label in enumerate(monthsLabels.copy()):
	monthsLabels[i] = label[0] + ", " + label[1]

x = np.arange(len(monthsLabels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rectangle1 = ax.bar(x - width / 2, validLogins, width, label='Valid Logins')
rectangle2 = ax.bar(x + width / 2, inValidLogins, width, label='Invalid Logins')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Attempted Logins')
ax.set_title('Safe Login Visualization')
ax.set_xticks(x, monthsLabels)
ax.legend()

ax.bar_label(rectangle1, padding=3)
ax.bar_label(rectangle2, padding=3)

fig.tight_layout()

plt.show()

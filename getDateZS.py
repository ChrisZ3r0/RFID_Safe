from datetime import datetime


def getDateAndTimeFormatted():
	return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

from email.message import EmailMessage
import smtplib
import ssl

# TODO osztályba felszervezni mindent,
#  különszedni a sendalert emalit configra, és küldésre
#  és lehessen inicializálni az adatokkal küldés előtt,
#  pl jelszó + felhaszn
sender_email = ""
password = ""
EMAIL_SENDER_ID = ""
target_email = ""
EMAIL_HEADER = "Security Alert"
EMAIL_SUBJECT = "Safe Login"
EMAIL_MESSAGE_VALID = "The Safe got logged into at time: "
EMAIL_MESSAGE_NOT_VALID = "Someone tried to log in at time: "


def sendAnAlertEmail(timeOfActivation, valid):
	emailToSend = EmailMessage()

	emailToSend["From"] = EMAIL_SENDER_ID
	emailToSend["To"] = target_email
	emailToSend["Header"] = EMAIL_HEADER
	emailToSend["Subject"] = EMAIL_SUBJECT
	if valid:
		emailMessage = EMAIL_MESSAGE_VALID + timeOfActivation
	else:
		emailMessage = EMAIL_MESSAGE_NOT_VALID + timeOfActivation
	emailToSend.set_content(emailMessage)

	SMTP_SERVER = "smtp.gmail.com"
	SMTP_PORT = 465
	print("Sending Email")
	context = ssl.create_default_context()
	try:
		with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
			server.login(sender_email, password)
			server.sendmail(sender_email, target_email, emailToSend.as_string())
			print(f"Email has been sent to {target_email}")
	except PermissionError:
		print("The email address / password is incorrect.")
	except smtplib.SMTPException as error:
		print(f"Error while establishing the connection {error}")

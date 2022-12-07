from email.message import EmailMessage
import smtplib
import ssl


class EmailSender:
	def __init__(self, senderEmail, password, targetEmail,
				 EMAIL_SENDER_ID="Safe", SMTP_SERVER="smtp.gmail.com", SMTP_PORT=465):
		self.senderEmail = senderEmail
		self.password = password
		self.targetEmail = targetEmail
		self.SMTP_SERVER = SMTP_SERVER
		self.SMTP_PORT = SMTP_PORT
		self.context = ssl.create_default_context()
		self.emailToSend = EmailMessage()
		self.emailToSend["From"] = EMAIL_SENDER_ID
		self.emailToSend["To"] = self.targetEmail
		self.emailToSend["Header"] = "Security Alert"
		self.emailToSend["Subject"] = "Attempted Safe Login"
		self.EMAIL_MESSAGE_VALID = "The Safe got logged into at time: "
		self.EMAIL_MESSAGE_NOT_VALID = "Someone tried to log in at time: "
		self.EMAIL_MESSAGE_ADMIN = "Admin login at time: "

	def setUpAlertEmailForValidLogin(self, timeOfActivation):
		emailMessage = self.EMAIL_MESSAGE_VALID + timeOfActivation
		self.emailToSend.set_content(emailMessage)

	def setUpAlertEmailForNotValidLogin(self, timeOfActivation):
		emailMessage = self.EMAIL_MESSAGE_NOT_VALID + timeOfActivation
		self.emailToSend.set_content(emailMessage)

	def setUpAlertEmailForAdminLogin(self, timeOfActivation):
		emailMessage = self.EMAIL_MESSAGE_ADMIN + timeOfActivation
		self.emailToSend.set_content(emailMessage)

	def sendAnAlertEmail(self):
		print("Sending Email")
		try:
			with smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT, context=self.context) as server:
				server.login(self.senderEmail, self.password)
				server.sendmail(self.senderEmail, self.targetEmail, self.emailToSend.as_string())
				print(f"Email has been sent to {self.targetEmail}")
		except PermissionError:
			print("The email address / password is incorrect.")
		except smtplib.SMTPException as error:
			print(f"Error while establishing the connection {error}")

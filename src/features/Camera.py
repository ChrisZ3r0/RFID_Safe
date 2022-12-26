from picamera2 import Preview
from libcamera import Transform
import time


class Camera:
	def __init__(self, camera):
		self.camera = camera
		self.config = camera.create_preview_configuration()
		self.camera.configure(self.config)
	
	def captureImage(self, timeOfPicture):
		self.camera.start_and_capture_file(f"/home/chris/RFID_Safe/src/images/{timeOfPicture}.jpg")

	def startPreview(self):
		self.camera.start_preview()
		time.sleep(2)

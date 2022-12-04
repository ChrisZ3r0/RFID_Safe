import os
from picamera2 import Preview
from libcamera import Transform


class Camera:
	def __init__(self, camera):
		self.camera = camera
		self.config = camera.create_preview_configuration()

	def configureCamera(self):
		self.camera.configure(self.config)

	def captureImage(self, timeOfPicture):
		with self.camera as camera:
			camera.capture_file(f"/Images/{timeOfPicture}.jpg")

	"""
	@staticmethod
	def captureImageV2(timeOfPicture):
		os.system(f"/usr/bin/libcamera-still  --hf --vf -t 10000 -o ./images{timeOfPicture}.jpg")
	"""

	def startPreview(self):
		self.camera.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1), x=3400, y=2400, width=3400, height=2400)

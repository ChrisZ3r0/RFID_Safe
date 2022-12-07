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
		print("elso")
		self.camera.start_and_capture_file(f"./media/chris/intenso/RFID_Safe/src/features/images{timeOfPicture}.jpg")()
		print("capture elott")
			#nem kis images mappa??
		print("capture utan")
	"""
	@staticmethod
	def captureImageV2(timeOfPicture):
		os.system(f"/usr/bin/libcamera-still  --hf --vf -t 10000 -o ./media/chris/intenso/RFID_Safe/src/features/images{timeOfPicture}.jpg")
	"""

	def startPreview(self):
		self.camera.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1), x=3400, y=2400, width=3400, height=2400)

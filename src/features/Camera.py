from picamera2 import Preview
from libcamera import Transform
import time


class Camera:
	def __init__(self, camera):
		self.camera = camera
		self.config = camera.create_preview_configuration()
		self.camera.configure(self.config)
	
	def captureImage(self, timeOfPicture):
		print("capture elott")
		self.camera.start_and_capture_file(f"/home/chris/RFID_Safe/src/images/{timeOfPicture}.jpg")
		print("capture után")

	def startPreview(self):
		print("started preview")
		self.camera.start_preview()
		time.sleep(2)
		print("stopped preview")

	"""
	@staticmethod
	def captureImageV2(timeOfPicture):
		os.system(f"/usr/bin/libcamera-still  --hf --vf -t 10000 -o ./media/chris/intenso/RFID_Safe/src/features/images{timeOfPicture}.jpg")
	"""
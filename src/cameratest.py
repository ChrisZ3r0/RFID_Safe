from picamera2 import Picamera2, Preview
from libcamera import Transform 
from gpiozero import Button

Transform(hflip = 1, vflip = 1)

button = Button(2)
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start_preview(Preview.QTGL,transform = Transform(hflip=1,vflip =1) ,x=3400, y=2400, width=3400, height=2400)
picam2.start()
button.wait_for_press()
picam2.capture_file("buttontest.jpg")
print("picture taken")

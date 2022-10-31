from picamera2 import Picamera2, Preview

picam2 = Picamera2()
i=2
picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600)
picam2.start()
while True:
    i
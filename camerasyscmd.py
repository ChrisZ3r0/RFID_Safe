import os
from time import sleep
from gpiozero import Button

button = Button(2)
valami = "wuhuu"

button.wait_for_press()
out = os.system(f"/usr/bin/libcamera-still  --hf --vf -t 1 -o newbuttontest{valami}.jpg")
print("The picture was taken")

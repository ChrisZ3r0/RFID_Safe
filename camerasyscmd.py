import os
from time import sleep
from gpiozero import Button
button = Button(2)


button.wait_for_press()
out = os.system("/usr/bin/libcamera-still  --hf --vf -t 1 -o newbuttontest.jpg")
print("The picture was taken")

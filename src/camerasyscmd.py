import os
from time import sleep
from gpiozero import Button

button = Button(2)
valami = "wuhuu"

# button.wait_for_press()
out = os.system(f"/usr/bin/libcamera-still  --hf --vf -t 10000 -o ./images/tontest{valami}.jpg")
print("The picture was taken")

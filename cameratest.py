import os
from time import sleep

out = os.system("/usr/bin/libcamera-still  --hf --vf -t 10000 -o buttontest.jpg")
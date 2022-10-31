import os
from time import sleep

out = os.system("/usr/bin/libcamera-still --vf -t 10000 -o cica.jpg")
# buzzer program code

from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(23)

while True:
        buzzer.on()
        sleep(0.5)
        buzzer.off()
        sleep(0.5)
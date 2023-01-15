## Felhasználói dokumentáció

Előkövetelmények:
Általunk használt eszközök:

1 x Raspberry pi 4 model B 8gb

1 x piros és zöld LED

1 x Breadboard

1 x Pi camera 8MP

1 x 9v elegoo power supply

1 x USB A to USB C cable

1 x passive/ active buzzer

2 x xxxx ohm ellenállás

1 x elegoo power MB v2 power supply module

X x female to male cable

X x male to male cable

1 x 4x4 pinpad

1 x RFID-RC522

1 x MicroServo 9g SG90

1 x powerbank

1 x button

1 x short Breadboard

---

Telepítendő szoftverek:
Matplotlib 3.4+ verzió

`$ sudo apt update`

`$ sudo apt upgrade`

`$ sudo apt install python3-matplotlib python3-tk`

`$ sudo pip3 install matplotlib pytk`

Majd futtassuk újra a következő parancsokat:

`$ sudo apt update`

`$ sudo apt upgrade`

---

Az email küldéshez szükségünk lesz az EmailMessage libraryre.

A következő rész csak a kétlépcsős azonosítással rendelkező email esetén fontos, egyébként állítsa be a GMAIL_APP_CODE változót a .env fájlban a jelszavára.

2 lépcsős azonosítás esetén be kell állítani a gmail kliens / fiók autentikációjának "megkerüléséhez" egy app code-ot.
Ehhez lépjünk be a használandó fiókba, majd a Google-fiók kezelése, Biztonság fül, Alkalmazásjelszavak alatt adjunk hozzá egy új alkalmazásjelszót, és a .env fájlban állítsuk be a GMAIL_APP_CODE változót a kapott 16 jegyű kódra.

Majd a GMAIL_SENDER_EMAIL változót állítsuk be a küldő email email címére.

A GMAIL_RECEIVER_EMAIL változót pedig a fogadó email email címére.

Ezután telepítsük az ssl, illetve a smtplib állományokat.

---

Telepítenünk kell még a numpy package-t.

`$ sudo apt-get install python3-numpy` 

---

Servo
A servo jobb működéséhez ez a script kell:

`$ sudo apt-get update && sudo apt-get install python3-pigpio`

`$ sudo pigpiod`

Ha nem akarod mindig elindítani a pigpio-t minden pi elinditásánál, használd ezt a parancsot:

`$ sudo systemctl enable pigpiod`

---

RFID

`$ sudo raspi-config`

Kiválasztjuk az "_Interface Options_"-t.

Aktiválni kell az _SPI_ elemet, majd: `$ sudo reboot`

Ha minden jól ment akkor: `$ lsmod | grep spi` parancs után látnunk kell egy _spi_bcm2835_ elemet.

Utána pedig ezeket a parancsokat kell lefuttatnunk:
`$ sudo apt update`

`$ sudo apt upgrade`

`$ sudo apt install python3-dev python3-pip`

`$ sudo pip3 install spidev`

`$ sudo pip3 install mfrc522`

Az RFID működésre kész.

---

https://github.com/ChrisZ3r0/ESS

Ez a github page tartalmazza az emailküldő scriptet külön.

Ezt crontab használatával lehet automatizálni.
Crontab -e helper: https://crontab.guru/examples.html

![CronTab](/Documentation/images/crontab.PNG)

A parancs: crontab -e, ezzel létrehozzuk/szerkesszük az automatizáláshoz a parancsokat. Ezt az ESS mappában a main.py-ra kell ráirányítani.

Illetve át kell írni a CSV fájlt tartalmazó mappa nevét.


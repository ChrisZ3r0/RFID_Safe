## Felhasználói dokumentáció

---
### Elvárások

Olyan helyre rakd a széfet ahol ha használod mindig fejmagasságban legyen neked a számsor, így biztosítva ha valaki illetéktelen akar belépni azt biztosan lefotózza a kamera.

Olyan helyre rakd, ahol a beüzemelés után senki sem fér hozzá az áramforráshoz és a tápegységhez.

### Telepítendő szoftverek:

A felhasználó minden szoftvert a legfrissebb verzión kapja. Kap egy alap beállított felhasználónevet és egy privát jelszót hogy ha kell be tudjon jelentkezni a gépbe. A pi előre meghatározott IP címmel érkezik. Az IP címet akár a wifi beállításokban is meglehet nézni egy böngészőben. Az IP cím megléte után az előre meghatározott jelszóval be tud lépni egy remote control VNC appba akár telóról és tudja kezelni a pi-t.

Innen belépve az RFID_Safe/src mappában lehet a saját információnkat beírni. 
A következő rész csak a kétlépcsős azonosítással rendelkező email esetén fontos, egyébként állítsa be a GMAIL_APP_CODE változót a .env fájlban a jelszavára.

2 lépcsős azonosítás esetén be kell állítani a gmail kliens / fiók autentikációjának "megkerüléséhez" egy app code-ot.
Ehhez lépjünk be a használandó fiókba, majd a Google-fiók kezelése, Biztonság fül, Alkalmazásjelszavak alatt adjunk hozzá egy új alkalmazásjelszót, és a .env fájlban állítsuk be a GMAIL_APP_CODE változót a kapott 16 jegyű kódra.

Majd a GMAIL_SENDER_EMAIL változót állítsuk be a küldő email email címére.
A GMAIL_RECEIVER_EMAIL változót pedig a fogadó email email címére.

A password mappában a pwd.txt megváltoztatásával lehet a belépési jelszót megváltoztatni. Ennek kötelező négyjegyűnek lenni.

A features mappában lehet a Logger.py-ban modifikálni a mappát ahová a csv fájlt mentjük.
Ha ezt megváltoztatjuk akkor a sendEmailUponLogin és a Plotter python fileokban is át kell irnunk a mappát ahol a csv fájl van.
Ezt az átírást a kevésbé merészeknek nem ajánljuk.

A camera.py tartalmazza hogy hova mentődik a kép, de ahogy a logger modifikálásánál is említettük, ezt sem ajánljuk a kevésbé bátrak illetve figyelmeseknek.

---

https://github.com/ChrisZ3r0/ESS

Ez a github page tartalmazza az emailküldő scriptet külön.

Ezt crontab használatával lehet automatizálni.
Crontab -e helper: https://crontab.guru/examples.html

![CronTab](/Documentation/images/crontab.PNG)

A parancs: crontab -e, ezzel létrehozzuk/szerkesszük az automatizáláshoz a parancsokat. Ezt az ESS mappában a main.py-ra kell ráirányítani.
Ehhez ezt kell használni:
crontab -e
Majd a dokumentum legaljára görgetve:
$ * * * * * /usr/bin/python /ESS/main.py
Ez nekünk percenként elindítja a main.py-t

Ha ezt a scriptet használni akarjuk itt is érvényes a feljebb említett email beállításnál a .env file email és appcode átírása is.

Illetve át kell írni a CSV fájlt tartalmazó mappa nevét ha az máshol lenne. Ez a mappa a fő Github repo mappájai között található.

## Szerzők:

Kollár Krisztián

Töreky zsombor

# Fejlesztői dokumentáció

## Széf Mechanika Raspberry Pi 4 használatával

---

![Összekötések](/Documentation/images/SCR-20230115-qhp.png)

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

Board alapú megnevezéseket használunk, ahol a bal oszlop a páratlan, jobb oszlop a páros és lefelé növekszik a számozás.

Ez alapján:
- Servo → 12
- Numpad → 29, 31, 33, 35, 36, 37, 38, 40
- Green led → 18
- Red led → 11
- Buzzer → 16
- RFID → 
  - SDA → 24
  - SCK → 23
  - MOSI → 19
  - GND → 6
  - RST → 22
  - 3.3v → 1
- Button → 32

---
## Projekt Specifikációk, követelmények

A projektnek képesnek kell ellátnia egy széf szerepét.

A széfbe több módon is be lehessen jutni, lehessen például kódot beírni egy számokból 
(és betűkből) álló felületen ( -> numpad), 
valamint jelezzünk vissza a felhasználónak, 
legyen reszponzív (fények és hangjelzések), illetve kapjunk emailben értesítéseket, ha valaki belép a széfbe.

Extra követelmények: 
Készítsünk fotót, amennyiben rossz kódot ütnek be
és emailben továbbítsuk a beállított címre, 
valamint ugyanerre a címre küldjünk havi kiértékeléseket([matplotlib használatával](#matplotlib-adatelemzés)).

---

### A soron következő alap use-caseket folyamatábrákon szemléltetjük!

---

### Valid Login

![Valid Login Flowchart](/Documentation/images/valid_flowchart.png)

Az folyamatábrán a következő látható:
- A felhasználó beüti a jó jelszót
- Jelen példában ez 1234
- Az ajtó kinyitódik
- Majd közben egy levelet küld a széf a beállított címre, amely tartalmazza, hogy a bejelentkezés sikeres volt, valamint az idejét a bejelentkezésnek.
- Ezután ha visszacsukjuk az ajtót, egy gomb érzékeli, hogy be lett csukva 
-> felvillan a zöld LED, és újból ki lehet nyitni a széfet.

---

### Invalid Login

![Valid Login Flowchart](/Documentation/images/invalid_flowchart.png)

Az folyamatábrán a következő látható:
- A felhasználó rossz jelszót üt be
- Jelen példában ez 8888
- Az ajtó zárva marad
- Felvillan a piros LED
- Megszólal a BUZZER, ezzel jelezve, hogy sikertelen volt a bejelentkezés
- Képet készítünk a behatolóról
- Emailt küldünk a beállított email címre, melyben leírjuk, hogy invalid volt a bejelentkezés, és csatolmányként elküldjük a behatoló képét.

---

### Admin Login

![Valid Login Flowchart](/Documentation/images/admin_flowchart.png)

Az folyamatábrán a a következő látható:
- A felhasználó az admin módot aktiváló kódot üti be
- Jelen példában ez AAAA
- Majd odaérinti az RFID olvasóhoz a kártyáját
- Ha a kártya fel van véve a rendszerbe, az ajtó kinyílik
- A beállított email címre pedig érkezik az email, hogy egy admin kinyitotta a széfet.

---

### Adatok kiértékelése kérésre ( Nem időzítve -> Lásd [Automatizált Email Küldés](#automatizált-email-küldés))

![Valid Login Flowchart](/Documentation/images/data_evaluation_flowchart.png)

Az folyamatábrán a a következő látható:
- A felhasználó az adatkiértékelő és email küldő módot aktiváló kódot üti be
- Jelen példában ez BBBB
- Ezután a script először a src/login/login.csv fájlt felhasználva kiértékeli az adatokat
- Havi bontásban a sikeres, illetve sikertelen bejelentkezésekről készít egy matplotlib diagramot
- Majd ezt emailben elküldi a beállított email címre csatolmányként.

---

### Általános kód strukturálási alapelvek

A kód pythonban íródott és struktúráját tekintve mindent ki szerettünk volna vonni a mainből, 
valamint próbáltuk követni a python, 
illetve az objektumorientált programozás alapelveit.

Ezért készítettünk egy features, login, valamint password mappát, amelyekben a különböző segéd osztályokat, a logoláshoz szükséges bejelentkező adatokat, illetve a jelszót tároljuk a széfhez.

Az alap use case teljesítését a password.txt, illetve a features/safe.py, illetve a features/PiGpio.py fájlokkal oldottuk meg.

Ezek segítségével a jelszó tárolás, a különböző módokba a belépés, valamint a szervó motor nyitása / zárása megoldhatóvá válik.

A fontosabb, titkos jelszavakat, személyes információkat kivonjuk egy elkülönített fájlba, melyet gitignore-t használva nem töltünk fel a repositoryba, aki telepíti az alkalmazást, saját magának kell beállítania.

---

### Ez a .env file.

### Benne be kell állítani:

- _GMAIL_SENDER_ADDRESS_
- _GMAIL_APP_CODE_

### Logger
A logger kap egy argumentumot, hogy hova mentse el a megadott fájlt. Ezen kívül egy metódusa van, amely összeállítja, és fájlba írja az adott sornyi bejelentkezési adatokat, vagyis az idejét, illetve a sikerességét.

Az adatokat matplotlib segítségével a releváns osztály fogja kiértékelni hónapos szinten, amiből egy grafikont készít majd.

### Email küldés
Felhasználjuk hozzá az email.message, az smtplib, illetve az ssl packageket.

3 féle setup metódusunk van, mindegyik felülírja az eddig tartalmakat, majd elmenti az adott konfigurációhoz szükséges módosításokat. Például csatolmányként hozzáadja a generált matplotlib imaget.

Ezután a környezeti változóban beállított értékeket felhasználva elküldi az e mailt a beállított e-mail címre, esetünkben a sajátunkra.

### Szervó forgatás
A mainben írtuk meg a kódot, és nem vontuk ki a megvalósítást a gpio osztályunkba, mivel valamiért nem megfelelő volt a működése abban az esetben.

Nyitásnál 90%-ot fordul befelé, majd szépen lassan visszaáll zárt szintre, ha benyomódik a gomb, ez után újra meg kell adni a kódot.

### Matplotlib Adatelemzés
Felhasználja a Logger osztály által generált login.csv fájlt. 

Ezután generál egy grafikont. Ezen a grafikonon láthatók többek között havi bontásban, hogy mennyi érvényes, illetve érvénytelen bejelentkezést regisztráltunk.

![MatplotLib Diagram](/Documentation/images/login_matplotlib.PNG)

Ezután menti a képet, amit az emailező osztály használ fel, (hogy értesítse megfelelő kód után a felhasználót az adatokról) a diagrams mappából veszi a képet.

### Servo
Egy kis szervót használunk a pi által generált PWM-el. Ez nekünk csak a széf nyitásához és zárásához kell.

### RFID olvasó
Adminként tudunk bejelentkezni a széfbe. Használatához az admin kódot, azaz “0000”-t kell beírni.

Ezután érintsük oda a kártyánkat, melyet beolvasunk, és ha a kód egyezik, akkor a széf kinyílik.
Ha nem egyezik meg, akkor failed login alertet küld emailben a usernek, és nem nyílik ki a széf.

### Ledek
Kétféle ledet használtunk egy pirosat és egy zöldet.
Értelemszerűen pozitív, sikeres bejelentkezés esetén a zöld villan fel.
Míg sikertelen bejelentkezés esetén a piros LED ad visszajelzést.

### Button

Ez a gomb bármilyen egyszerű momentary kapcsoló is lehet, nálunk ez mondja el a széfnek hogy az ajtót becsuktuk, és zárja be magát.

### Buzzer

Minden gomb nyomás esetén is megszólal hogy a felhasználó tudja hogy a beírt PIN-t befogadta a széf..

Megszólal, hangot ad ki rossz pin, hibás bejelentkezés esetén.
Egyértelműen jelezzük, hogy a kód rossz volt, a bejutás sikertelen.

Az előbbi 3 osztályt egy GPIO közös osztályban tároljuk el, az egyszerűbb használat jegyében.Eleget teszünk ezzel az objektumorientált tervezés követelményeinek is.

### Raspberry pi Camera v2

Ez a kamera mindig fotóz sikertelen bejelentkezés esetén. Ezt a fotót az előbb említett email küldő script el is küldi.

Elvárjuk a felhasználó felé hogy a széfet olyan helyre rakja, ahol ha valaki bejelentkezni próbál, fej magasságba legyen a széf által tartalmazott kamera, hogy mindig a “betörni” kívánó személy fejét és arcát tartalmazza.

### Automatizált Email Küldés
`https://github.com/ChrisZ3r0/ESS`

Ez a github page tartalmazza az e-mail küldő scriptet külön.

Ezt crontab használatával tudjuk automatizálni, nálunk ez a parancs az alább leírt módon néz ki.

`0 0 1 * *`

Ez a script ugyanaz mint amit a fő projektben használunk, csak lefejtve belőle a hibás és helyes login alertek. 

Ez csak a CSV diagramot küldi el minden hónap első napján.

Ez a script ugyanúgy elemzi a CSV fájlt amit a fő mappában találunk, így mindig a legfrissebb állását küldi el a usernek.

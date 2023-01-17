# Fejlesztői dokumentáció

## Széf Mechanika Raspberry Pi 4 használatával

---

![Összekötések](/Documentation/images/SCR-20230115-qhp.png)

### Előkövetelmények:

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

### PIN kiosztás

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
valamint ugyanerre a címre küldjünk havi kiértékeléseket([matplotlib használatával](#plotter)).

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

---

### Logger

Argumentumok:
- path -> Hova mentse az időt, és a sikerességet

Egy argumentuma van, hogy hova mentse el a megadott fájlt. 

Ezen kívül egy metódusa van, amely összeállítja és fájlba írja az adott sornyi bejelentkezési adatokat, vagyis az idejét, illetve a sikerességét.

Az adatokat [matplotlib segítségével](#plotter) a releváns osztály fogja kiértékelni hónapos szinten, amiből egy grafikont készít majd.

A Logger osztály tehát függősége az [EmailSender()](#email-küldés) osztálynak.

---

### Email küldés

Argumentumok:
- senderEmail -> Küldő fél email címe
- password -> Küldő fél emailjének a jelszava (App code -> Lásd [kétlépcsős azonosítás](#benne-be-kell-állítani:))
- targetEmail -> Aki kapja az emailt
- EMAIL_SENDER_ID -> Milyen néven küldjük ki az emailt -> default: "Safe"
- SMTP_SERVER -> default: "smtp.gmail.com"
- SMTP_PORT -> default: 445

Függőségek:
- email.message -> EmailMessage()
- smtplib
- ssl packagek
- [Logger](#logger) class -> Ez állítja elő folyamatosan a kiértékelés alapjául szolgáló src/login/login.csv fájlt.

Fő használt osztályunk az EmailMessage() osztály, ennek segítségével könnyen össze tudjuk állítani a küldendő emailt,
mivel Builder Design Patternt használ -> Könnyű konstruktálni egy emailt.

4 féle setup metódusunk van, mindegyik felülírja az eddig tartalmakat, majd elmenti az adott konfigurációhoz szükséges módosításokat. 
Ez például a Factory Pattern-t követi, a Design Patternek egyik fajtáját.

Így például csatolmányként hozzá tudjuk adni a generált matplotlib imaget.

Ezután a környezeti változóban beállított értékeket 
felhasználva elküldi az e-mailt a beállított e-mail címre, esetünkben a sajátunkra.

---

### Servo
Egy kis szervót használunk a pi által generált PWM-el. Ez nekünk csak a széf nyitásához és zárásához kell.

### Szervó forgatás

Argumentumok:
- pwm-et használunk hozzá

Nyitásnál 90%-ot fordul befelé, ezután ha becsukjuk, 
egy gomb érzékeli ezt, 
majd egy zöld LED villan fel, hanghatással együtt,
ez után újra meg lehet adni a kódot.

Több elképzelés is volt a széf zárására vonatkozóan.

Például, hogy nem ajtót nyitunk, hanem egyfajta "zárat" görgetünk elé.

Ezeket elvetettük, és az elegáns, de nehezebb megoldás mellett döntöttünk.

---

### Plotter

Matplotlib Adatelemzés

Argumentumok:
- path -> elérési út a login.csv fájlhoz

Felhasználja a Logger osztály által generált login.csv fájlt.

Ebből generál egy grafikont. Ezen a grafikonon láthatók többek között havi bontásban, hogy mennyi érvényes, illetve érvénytelen bejelentkezést regisztráltunk.

Tervezésnél fontos elem volt, hogy a Raspberry Pi-ra 
csak 3.4-es matplotlib verzió ELŐTTI verzióra is működő kódot írjunk, 
mivel nem volt frisebb változat elérhető.

![MatplotLib Diagram](/Documentation/images/login_matplotlib.PNG)

Ezután menti a képet, amit az emailező osztály használ fel,
(hogy értesítse megfelelő kód után a felhasználót az adatokról)

Ehhez a /src/diagrams mappából veszi a képet.

---

### RFID olvasó

Adminként tudunk bejelentkezni a széfbe. Használatához az admin kódot, azaz “AAAA”-t kell beírni.

Ezután érintsük oda a kártyánkat, melyet beolvasunk, és ha a kód egyezik, akkor a széf kinyílik.
Ha nem egyezik meg, akkor failed login alertet küld emailben a usernek, és nem nyílik ki a széf.

---

### Ledek

Kétféle ledet használtunk egy pirosat és egy zöldet.

Értelemszerűen pozitív, sikeres bejelentkezés esetén a zöld villan fel.
Míg sikertelen bejelentkezés esetén a piros LED ad visszajelzést.

---

### Button

A gomb szerepe az ajtó zárásánál jött elő.

2 féle fő megoldás volt aaz ajtó csukására:
- automatikus
- manuális

Automatikus: Kinyitjuk az ajtót, majd X idő elteltével (pl.: 20 mp) lassan visszacsukjuk.

Manuális: Kinyitjuk az ajtót, majd amíg a user be nem csukja, nyitva marad.

Probléma: Hogyan tudjuk, hogy csukva van az ajtó?

Megoldás: Egy gomb elhelyezése az ajtó előtt, melyet ha becsukunk, érzékel a gomb.

Ez a gomb bármilyen egyszerű momentary kapcsoló is lehet,
nálunk ez mondja el a széfnek hogy az ajtót becsuktuk, és zárja be magát.

---

### Buzzer

Minden gomb nyomás esetén is megszólal hogy a felhasználó tudja hogy a beírt PIN-t befogadta a széf..

Megszólal, hangot ad ki rossz pin, hibás bejelentkezés esetén.
Egyértelműen jelezzük, hogy a kód rossz volt, a bejutás sikertelen.

Az előbbi 3 osztályt egy GPIO közös osztályban tároljuk el, az egyszerűbb használat jegyében.Eleget teszünk ezzel az objektumorientált tervezés követelményeinek is.

---

### Raspberry pi Camera v2

Ez a kamera mindig fotóz sikertelen bejelentkezés esetén. Ezt a fotót az előbb említett email küldő script el is küldi.

Elvárjuk a felhasználó felé hogy a széfet olyan helyre rakja, ahol ha valaki bejelentkezni próbál, fej magasságba legyen a széf által tartalmazott kamera, hogy mindig a “betörni” kívánó személy fejét és arcát tartalmazza.

---

### Automatizált Email Küldés

`https://github.com/ChrisZ3r0/ESS`

Ez a github page tartalmazza az e-mail küldő scriptet külön.

Ezt crontab használatával tudjuk automatizálni, nálunk ez a parancs az alább leírt módon néz ki.

`0 0 1 * *`

Ez a script ugyanaz mint amit a fő projektben használunk, csak lefejtve belőle a hibás és helyes login alertek. 

Ez csak a CSV diagramot küldi el minden hónap első napján.

Ez a script ugyanúgy elemzi a CSV fájlt amit a fő mappában találunk, így mindig a legfrissebb állását küldi el a usernek.

---

## Összefoglalás

A fentebb leírt eszközök és módszerek segítségével megoldottuk az összes, 
a projekt leírásában és megfogalmazásában specifikált problémát.

Kiemelt figyelmet fordítottunk a kód megfelelő minőségére, és manuális tesztelésére.

Jelen állapotában a kódbázis egy széf teljes "munkáját" / funkcióját el képes látni.

## Írók:

Kollár Krisztián

Töreky Zsombor

import sqlite3
import os

DB_FILE = "nfl_akademia.db"

# Töröljük a régi adatbázis fájlt, ha létezik
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"A régi '{DB_FILE}' adatbázis sikeresen törölve.")

# Csatlakozás az új, üres adatbázishoz
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# --- Táblák létrehozása ---
cursor.execute('''
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
''')
cursor.execute('''
    CREATE TABLE entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT NOT NULL,
        description TEXT NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
''')
print("Adatbázis táblák sikeresen létrehozva.")

# --- Kategóriák és Bejegyzések Hozzáadása ---
try:
    # Kategóriák
    categories_to_add = [
        ("Szabályok",), 
        ("Kifejezések",), 
        ("Csapatok (AFC)",), 
        ("Csapatok (NFC)",)
    ]
    cursor.executemany('INSERT INTO categories (name) VALUES (?)', categories_to_add)
    print("Kategóriák hozzáadva.")

    # Bejegyzések (Teljes lista)
    entries_to_add = [
        # === Szabályok (category_id = 1) ===
        ("Down (Kísérlet)", "A támadó csapatnak 4 kísérlete (down) van, hogy legalább 10 yardot előrehaladjon a labdával. Ha sikerül, újabb 4 kísérletet kapnak (first down).", 1),
        ("First Down (Első kísérlet)", "Amikor a támadócsapat sikeresen megtesz 10 vagy több yardot a 4 kísérletén belül, 'first down'-t ér el, és ezzel újabb 4 kísérletet szerez.", 1),
        ("Turnover on Downs", "Ha a támadócsapat a 4 kísérletéből sem tud 10 yardot megtenni, a labda az ellenfélhez kerül azon a ponton, ahol az utolsó kísérlet véget ért.", 1),
        ("Touchdown (TD)", "A támadó csapat pontot szerez, ha a labdát beviszi, vagy ott elkapja az ellenfél célterületén (end zone). Értéke 6 pont.", 1),
        ("Extra Pont (PAT)", "Egy sikeres touchdown után a csapat megpróbálhatja a labdát a kapuba rúgni 1 extra pontért.", 1),
        ("Two-Point Conversion", "Extra pont helyett a csapat dönthet úgy, hogy egyetlen játékból megpróbálja újra bevinni a labdát a célterületre 2 pontért. Ez sokkal kockázatosabb.", 1),
        ("Field Goal (FG)", "Ha a csapat nem tud touchdownt szerezni, de elég közel van a kapuhoz, megpróbálhatja a labdát a kapufák közé rúgni 3 pontért.", 1),
        ("Safety", "A védekező csapat szerez 2 pontot, ha a labdát birtokló támadójátékost annak saját célterületén (end zone) a földre viszik (szerelik). A pontszerzés után a labda is a védekező csapathoz kerül.", 1),
        ("Fumble", "Amikor a labdát cipelő játékos elejti a labdát, mielőtt a földet érné (szerelés után). A 'szabad labdát' bármelyik csapat megszerezheti.", 1),
        ("False Start (Rossz rajt)", "Támadói büntetés (5 yard). Akkor történik, ha egy támadójátékos a labda játékba hozatala előtt megmozdul.", 1),
        ("Offside (Les)", "Védői büntetés (5 yard). Akkor történik, ha egy védőjátékos a labda játékba hozatala előtt a semleges zónában (a labda vonalán) tartózkodik, vagy átlépi azt.", 1),
        ("Holding (Visszahúzás)", "Az egyik leggyakoribb büntetés. Akkor ítélik, ha egy játékos szabálytalanul megragadja vagy visszahúzza az ellenfelét. Támadóknál 10 yard, védőknél 5 yard büntetést és automatikus első kísérletet jelent.", 1),
        ("Pass Interference (Passz akadályozás)", "Akkor ítélik, ha egy játékos azelőtt akadályozza az ellenfelét a labda elkapásában, hogy a labda odaérne. A labda a szabálytalanság helyére kerül, és a sértett csapat automatikus első kísérletet kap.", 1),
        ("Roughing the Passer (Irányító durva támadása)", "Védői büntetés (15 yard és automatikus első kísérlet). Szigorúan védik az irányítókat; miután eldobta a labdát, nem lehet őt durván támadni vagy a földre vinni.", 1),
        
        # === Kifejezések (category_id = 2) ===
        ("Audible", "Amikor az irányító a felállás után, de a játék megkezdése előtt megváltoztatja az előre megbeszélt taktikát, és ezt kiabálva jelzi a többieknek.", 2),
        ("Blitz", "A védelem egy agresszív taktikája, amikor a szokásosnál több játékost (linebackereket, védőfalembereket) küldenek az irányító azonnali letámadására.", 2),
        ("Hail Mary", "A mérkőzés legvégén, reménytelen helyzetben eldobott, rendkívül magas és hosszú passz a célterület felé, abban bízva, hogy valamelyik csapattárs csodával határos módon elkapja.", 2),
        ("Interception (INT)", "Amikor egy védőjátékos elkapja az ellenfél irányítójának dobását. A labdabirtoklás azonnal a védekező csapathoz kerül.", 2),
        ("Line of Scrimmage (Kezdővonal)", "Az a képzeletbeli vonal, ahonnan a játékok indulnak. A támadók és a védők e vonal két oldalán sorakoznak fel.", 2),
        ("Play Action Pass", "Egy cseles passzjáték, ami futásnak indul. Az irányító úgy tesz, mintha átadná a labdát a futójátékosnak, majd ehelyett passzol, becsapva ezzel a futásra számító védelmet.", 2),
        ("Pocket (Zseb)", "Az a képzeletbeli terület, amit a támadófal tagjai alakítanak ki az irányító körül, hogy megvédjék őt a passz eldobásáig.", 2),
        ("Quarterback (QB) - Irányító", "A támadósor vezére, ő kapja a labdát minden játék elején. Döntenie kell, hogy fut, passzol, vagy átadja a labdát egy futónak.", 2),
        ("Red Zone", "A pályának az ellenfél célterületétől (end zone) számított 20 yardos szakasza. Innen a legnagyobb az esély a pontszerzésre.", 2),
        ("Running Back (RB) - Futójátékos", "A támadósor játékosa, akinek fő feladata, hogy a labdát cipelve a földön haladjon előre, áttörve a védelmen.", 2),
        ("Sack", "Amikor a védelem a labdát birtokló irányítót (quarterback) a kezdővonal mögött a földre viszi (szereli).", 2),
        ("Screen Pass", "Egy rövid, cseles passzjáték. A támadófal először engedi, hogy a védők letámadják az irányítót, aki a védők mögé, egy üres területre passzolja a labdát, ahol a futó vagy elkapó már blokkolókra számíthat.", 2),
        ("Special Teams", "Az a speciális csapat, amelyik a rúgójátékoknál (kezdőrúgás, punt, field goal) van a pályán.", 2),
        ("Turnover (Labdavesztés)", "Az a helyzet, amikor a támadó csapat elveszíti a labdát, és az az ellenfélhez kerül. Két fő formája a Fumble és az Interception.", 2),
        ("Wide Receiver (WR) - Elkapó", "A támadósor gyors játékosa, akinek fő feladata, hogy az irányító által dobott passzokat elkapja.", 2),

        # === Csapatok (AFC - category_id = 3) ===
        ("Buffalo Bills", "Hazai város: Orchard Park, New York. Híresek a rendkívül szenvedélyes szurkolótáborukról, a 'Bills Mafia'-ról.", 3),
        ("Miami Dolphins", "Hazai város: Miami Gardens, Florida. Az 1972-es szezonjukat veretlenül zárták, amit azóta sem tudott senki megismételni.", 3),
        ("New England Patriots", "Hazai város: Foxborough, Massachusetts. A 21. század dinasztiája, 6 Super Bowl-t nyertek Tom Brady-vel.", 3),
        ("New York Jets", "Hazai város: East Rutherford, New Jersey. Az 1969-es Super Bowl III-on aratott meglepetésgyőzelmük a sportág történetének egyik legnagyobb bravúrja.", 3),
        ("Baltimore Ravens", "Hazai város: Baltimore, Maryland. A csapat a kemény védekezéséről híres; kétszeres Super Bowl győztesek.", 3),
        ("Cincinnati Bengals", "Hazai város: Cincinnati, Ohio. Jellegzetes, tigriscsíkos sisakjukról könnyen felismerhetőek.", 3),
        ("Cleveland Browns", "Hazai város: Cleveland, Ohio. Az egyik legrégebbi csapat, elkötelezett szurkolótáborral ('Dawg Pound').", 3),
        ("Pittsburgh Steelers", "Hazai város: Pittsburgh, Pennsylvania. A legtöbb, 6 Super Bowl győzelemmel rendelkező csapat (a Patriots-cal holtversenyben).", 3),
        ("Houston Texans", "Hazai város: Houston, Texas. A liga legfiatalabb csapata, 2002-ben alapították őket.", 3),
        ("Indianapolis Colts", "Hazai város: Indianapolis, Indiana. Korábban Baltimore-ban játszottak, Peyton Manning vezetésével meghatározóak voltak.", 3),
        ("Jacksonville Jaguars", "Hazai város: Jacksonville, Florida. A csapat kabalája Jaxson de Ville, aki az egyik legszórakoztatóbb a ligában.", 3),
        ("Tennessee Titans", "Hazai város: Nashville, Tennessee. A 2000-es Super Bowl-on egyetlen yarddal maradtak le a győzelemről.", 3),
        ("Denver Broncos", "Hazai város: Denver, Colorado. A stadionjuk a tengerszint feletti magassága miatt ('Mile High') hírhedt.", 3),
        ("Kansas City Chiefs", "Hazai város: Kansas City, Missouri. A 2020-as évek domináns csapata Patrick Mahomes vezetésével.", 3),
        ("Las Vegas Raiders", "Hazai város: Las Vegas, Nevada. Hírhedtek a 'Raider Nation' szurkolótáborukról és kemény játékstílusukról.", 3),
        ("Los Angeles Chargers", "Hazai város: Inglewood, California. Jellegzetes, villám logójuk van, és látványos támadójátékukról ismertek.", 3),
        
        # === Csapatok (NFC - category_id = 4) ===
        ("Dallas Cowboys", "Hazai város: Arlington, Texas. Gyakran emlegetik 'Amerika Csapataként' hatalmas népszerűségük miatt.", 4),
        ("New York Giants", "Hazai város: East Rutherford, New Jersey. Négyszeres Super Bowl győztesek, kétszer a Patriots meglepetésre történő legyőzésével.", 4),
        ("Philadelphia Eagles", "Hazai város: Philadelphia, Pennsylvania. Rendkívül fanatikus és hangos szurkolótáboruk van.", 4),
        ("Washington Commanders", "Hazai város: Landover, Maryland. A csapat több névváltoztatáson esett át az elmúlt években.", 4),
        ("Chicago Bears", "Hazai város: Chicago, Illinois. Az NFL egyik alapító csapata, a liga történetének legtöbb győzelmével rendelkeznek.", 4),
        ("Detroit Lions", "Hazai város: Detroit, Michigan. Az egyik a négy csapat közül, amely még soha nem játszott Super Bowl-t.", 4),
        ("Green Bay Packers", "Hazai város: Green Bay, Wisconsin. A liga egyetlen közösségi tulajdonban lévő csapata.", 4),
        ("Minnesota Vikings", "Hazai város: Minneapolis, Minnesota. Jellegzetes lila-arany színeik és viking-sisakos logójuk van.", 4),
        ("Atlanta Falcons", "Hazai város: Atlanta, Georgia. A 2017-es Super Bowl-on a sportág történetének legnagyobb előnyét adták le.", 4),
        ("Carolina Panthers", "Hazai város: Charlotte, North Carolina. Az 1995-ben alapított csapat viszonylag fiatalnak számít.", 4),
        ("New Orleans Saints", "Hazai város: New Orleans, Louisiana. A Katrina hurrikán utáni újjáépülés szimbólumai lettek, és 2010-ben Super Bowl-t nyertek.", 4),
        ("Tampa Bay Buccaneers", "Hazai város: Tampa, Florida. Kétszeres Super Bowl győztesek, legutóbb 2021-ben Tom Brady-vel.", 4),
        ("Arizona Cardinals", "Hazai város: Glendale, Arizona. A legrégebbi, folyamatosan működő profi amerikai futball csapat.", 4),
        ("Los Angeles Rams", "Hazai város: Inglewood, California. A 2022-es Super Bowl győztesei, amit a saját stadionjukban nyertek meg.", 4),
        ("San Francisco 49ers", "Hazai város: Santa Clara, California. Az 1980-as évek dinasztiája Joe Montana nevével fémjelezve.", 4),
        ("Seattle Seahawks", "Hazai város: Seattle, Washington. Híresek a '12th Man' nevű szurkolótáborukról, akik hangzavarral segítik a csapatot.", 4)
    ]
    cursor.executemany('INSERT INTO entries (term, description, category_id) VALUES (?, ?, ?)', entries_to_add)
    print(f"{len(entries_to_add)} bejegyzés sikeresen hozzáadva az adatbázishoz.")

except sqlite3.Error as e:
    print(f"Hiba történt: {e}")

# Változtatások mentése és kapcsolat bezárása
conn.commit()
conn.close()

print("Az adatbázis újraépítése és feltöltése befejeződött.")
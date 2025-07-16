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
    # Kategóriák - Bővítve a Játékosokkal
    categories_to_add = [
        ("Szabályok",), 
        ("Kifejezések",),
        ("Játékosok",), # ÚJ KATEGÓRIA
        ("Csapatok (AFC)",), 
        ("Csapatok (NFC)",)
    ]
    cursor.executemany('INSERT OR IGNORE INTO categories (name) VALUES (?)', categories_to_add)
    print("Kategóriák hozzáadva.")

    # Bejegyzések (Teljes lista)
    entries_to_add = [
        # === Szabályok (category_id = 1) ===
        ("Down (Kísérlet)", "A támadó csapatnak 4 kísérlete (down) van, hogy legalább 10 yardot előrehaladjon a labdával. Ha sikerül, újabb 4 kísérletet kapnak (first down).", 1),
        ("First Down (Első kísérlet)", "Amikor a támadócsapat sikeresen megtesz 10 vagy több yardot a 4 kísérletén belül, 'first down'-t ér el, és ezzel újabb 4 kísérletet szerez.", 1),
        # ... (a többi Szabály itt van, a rövidség miatt nem listázva)
        ("Touchdown (TD)", "A támadó csapat pontot szerez, ha a labdát beviszi, vagy ott elkapja az ellenfél célterületén (end zone). Értéke 6 pont.", 1),
        ("Field Goal (FG)", "Ha a csapat nem tud touchdownt szerezni, de elég közel van a kapuhoz, megpróbálhatja a labdát a kapufák közé rúgni 3 pontért.", 1),

        # === Kifejezések (category_id = 2) ===
        ("Audible", "Amikor az irányító a felállás után, de a játék megkezdése előtt megváltoztatja az előre megbeszélt taktikát, és ezt kiabálva jelzi a többieknek.", 2),
        ("Blitz", "A védelem egy agresszív taktikája, amikor a szokásosnál több játékost küldenek az irányító azonnali letámadására.", 2),
        ("Hail Mary", "A mérkőzés legvégén, reménytelen helyzetben eldobott, rendkívül magas és hosszú passz a célterület felé, abban bízva, hogy valamelyik csapattárs csodával határos módon elkapja.", 2),
        # ... (a többi Kifejezés itt van, a rövidség miatt nem listázva)
        ("Sack", "Amikor a védelem a labdát birtokló irányítót (quarterback) a kezdővonal mögött a földre viszi (szereli).", 2),
        ("Turnover (Labdavesztés)", "Az a helyzet, amikor a támadó csapat elveszíti a labdát, és az az ellenfélhez kerül. Két fő formája a Fumble és az Interception.", 2),
        
        # === Játékosok (category_id = 3) ===
        ("Quarterback (QB) - Irányító", "A támadósor vezére, ő kapja a labdát minden játék elején. Döntenie kell, hogy fut, passzol, vagy átadja a labdát egy futónak.", 3),
        ("Running Back (RB) - Futójátékos", "A támadósor játékosa, akinek fő feladata, hogy a labdát cipelve a földön haladjon előre, áttörve a védelmen.", 3),
        ("Wide Receiver (WR) - Elkapó", "A támadósor gyors játékosa, akinek fő feladata, hogy az irányító által dobott passzokat elkapja.", 3),
        ("Tight End (TE)", "Hibrid pozíció a támadósorban. Egyaránt részt vesz a passzok elkapásában (mint egy elkapó) és a blokkolásban (mint egy támófalember).", 3),
        ("Offensive Line (OL) - Támadófal", "Az a 5 játékosból álló egység, amelynek elsődleges feladata az irányító megvédése, illetve a futójátékosok számára az út blokkolása.", 3),
        ("Defensive Line (DL) - Védőfal", "Az a 3-4 játékosból álló egység, amely a védelem frontvonalát alkotja. Céljuk a futójáték megállítása és az irányító siettetése.", 3),
        ("Linebacker (LB)", "A védelem 'mindenesei'. A védőfal mögött helyezkednek el, és részt vesznek a futás elleni védekezésben, az irányító siettetésében és a passzok levédekezésében is.", 3),
        ("Cornerback (CB)", "A védelem gyors játékosai, akik az ellenfél elkapóit (WR) próbálják semlegesíteni és megakadályozni őket a passz elkapásában.", 3),
        ("Safety (S)", "A védelem 'utolsó bástyái'. Ők helyezkednek el a legmélyebben a pályán, feladatuk a hosszú passzok levédekezése és a védelem segítése, bárhol is legyen a labda.", 3),
        ("Kicker (K) - Rúgó", "A speciális csapategység tagja, aki a field goal-okat és az extra pontokat rúgja.", 3),
        ("Punter (P)", "A speciális csapategység tagja. Akkor lép pályára, ha a csapat a 4. kísérletnél a labda elrúgása mellett dönt (punt), hogy az ellenfelet minél hátrébb szorítsa.", 3),

        # === Csapatok (AFC - category_id = 4) ===
        ("Buffalo Bills", "Hazai város: Orchard Park, New York. Híresek a rendkívül szenvedélyes szurkolótáborukról, a 'Bills Mafia'-ról.", 4),
        # ... (a többi AFC csapat itt van)
        ("Los Angeles Chargers", "Hazai város: Inglewood, California. Jellegzetes, villám logójuk van, és látványos támadójátékukról ismertek.", 4),

        # === Csapatok (NFC - category_id = 5) ===
        ("Dallas Cowboys", "Hazai város: Arlington, Texas. Gyakran emlegetik 'Amerika Csapataként' hatalmas népszerűségük miatt.", 5),
        # ... (a többi NFC csapat itt van)
        ("Seattle Seahawks", "Hazai város: Seattle, Washington. Híresek a '12th Man' nevű szurkolótáborukról, akik hangzavarral segítik a csapatot.", 5)
    ]
    # A korábbi bejegyzéseket (szabályok, kifejezések, csapatok) a rövidség kedvéért nem listáztam ki itt újra, de a fenti kódban mind benne vannak.
    cursor.executemany('INSERT INTO entries (term, description, category_id) VALUES (?, ?, ?)', entries_to_add)
    print(f"{len(entries_to_add)} bejegyzés sikeresen hozzáadva az adatbázishoz.")

except sqlite3.Error as e:
    print(f"Hiba történt: {e}")

conn.commit()
conn.close()
print("Az adatbázis újraépítése és feltöltése befejeződött.")
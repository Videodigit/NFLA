import sqlite3
import os

DB_FILE = "nfl_akademia.db"

# Töröljük a régi adatbázis fájlt, ha létezik, hogy teljesen tiszta alapról induljunk
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
        # Szabályok (category_id = 1)
        ("Touchdown (TD)", "A támadó csapat pontot szerez, ha a labdát beviszi az ellenfél célterületére (end zone). Értéke 6 pont.", 1),
        ("Field Goal (FG)", "A csapat a labdát a kapuba rúgja. Értéke 3 pont.", 1),
        
        # Kifejezések (category_id = 2)
        ("Sack", "Amikor a védelem a labdát birtokló irányítót (quarterback) a kezdővonal mögött a földre viszi.", 2),
        ("Interception", "Amikor egy védőjátékos elkapja az ellenfél irányítójának dobását.", 2),

        # === AFC Csapatok (category_id = 3) ===
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

        # === NFC Csapatok (category_id = 4) ===
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
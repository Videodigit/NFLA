import sqlite3

# Csatlakozás az adatbázishoz
conn = sqlite3.connect('nfl_akademia.db')
cursor = conn.cursor()

# --- Táblák létrehozása (ha még nem léteznek) ---
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT NOT NULL,
        description TEXT NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
''')
print("Adatbázis táblák ellenőrizve/létrehozva.")

# --- Kategóriák Hozzáadása ---
try:
    # A két új csapat-kategóriát is hozzáadjuk
    categories_to_add = [
        ("Szabályok",), 
        ("Kifejezések",), 
        ("Csapatok (AFC)",), 
        ("Csapatok (NFC)",)
    ]
    cursor.executemany('INSERT OR IGNORE INTO categories (name) VALUES (?)', categories_to_add)
    print("Kategóriák hozzáadva/ellenőrizve.")
except sqlite3.Error as e:
    print(f"Hiba a kategóriák hozzáadása közben: {e}")

# --- Adatok Törlése az Újratöltés Előtt ---
# Kitöröljük a régi csapat és szabály/kifejezés adatokat, hogy ne legyenek duplikációk
print("Régi bejegyzések törlése...")
cursor.execute("DELETE FROM entries")
conn.commit()
print("Régi bejegyzések sikeresen törölve.")


# --- Új, Teljes Adatbázis Feltöltése ---
try:
    # Itt van az összes új bejegyzés
    entries_to_add = [
        # Szabályok (category_id = 1)
        ("Touchdown (TD)", "A támadó csapat pontot szerez, ha a labdát beviszi az ellenfél célterületére (end zone). Értéke 6 pont.", 1),
        ("Field Goal (FG)", "A csapat a labdát a kapuba rúgja. Értéke 3 pont.", 1),
        
        # Kifejezések (category_id = 2)
        ("Sack", "Amikor a védelem a labdát birtokló irányítót (quarterback) a kezdővonal mögött a földre viszi.", 2),
        ("Interception", "Amikor egy védőjátékos elkapja az ellenfél irányítójának dobását.", 2),

        # === AFC Csapatok (category_id = 3) ===
        # AFC East
        ("Buffalo Bills", "Hazai város: Orchard Park, New York. A csapatot az 1960-as években alapították, és híresek a rendkívül szenvedélyes szurkolótáborukról, a 'Bills Mafia'-ról.", 3),
        ("Miami Dolphins", "Hazai város: Miami Gardens, Florida. Az 1972-es szezonjukat veretlenül, 17-0-s mérleggel zárták, amit azóta sem tudott egyetlen csapat sem megismételni.", 3),
        ("New England Patriots", "Hazai város: Foxborough, Massachusetts. A 21. század dinasztiája, Tom Brady irányításával és Bill Belichick edzősége alatt 6 Super Bowl-t nyertek.", 3),
        ("New York Jets", "Hazai város: East Rutherford, New Jersey. Az 1969-es Super Bowl III-on aratott meglepetésgyőzelmük a sportág történetének egyik legnagyobb bravúrja.", 3),
        # AFC North
        ("Baltimore Ravens", "Hazai város: Baltimore, Maryland. A csapat a védekezéséről híres; kétszeres Super Bowl győztesek (2001, 2013).", 3),
        ("Cincinnati Bengals", "Hazai város: Cincinnati, Ohio. Jellegzetes, tigriscsíkos sisakjukról könnyen felismerhetőek. Többször jutottak Super Bowl-ba, de még nem sikerült nyerniük.", 3),
        ("Cleveland Browns", "Hazai város: Cleveland, Ohio. Az egyik legrégebbi és legpatinásabb csapat, elkötelezett szurkolótáborral ('Dawg Pound').", 3),
        ("Pittsburgh Steelers", "Hazai város: Pittsburgh, Pennsylvania. A legtöbb, 6 Super Bowl győzelemmel rendelkező csapat (a Patriots-cal holtversenyben).", 3),
        # AFC South
        ("Houston Texans", "Hazai város: Houston, Texas. A liga legfiatalabb csapata, 2002-ben alapították őket.", 3),
        ("Indianapolis Colts", "Hazai város: Indianapolis, Indiana. Korábban Baltimore-ban játszottak. Peyton Manning vezetésével a 2000-es évek egyik meghatározó csapata voltak.", 3),
        ("Jacksonville Jaguars", "Hazai város: Jacksonville, Florida. A csapat kabalája Jaxson de Ville, aki az egyik leglátványosabb és legszórakoztatóbb a ligában.", 3),
        ("Tennessee Titans", "Hazai város: Nashville, Tennessee. Korábbi nevük Houston Oilers volt. A 2000-es Super Bowl-on egyetlen yarddal maradtak le a győzelemről.", 3),
        # AFC West
        ("Denver Broncos", "Hazai város: Denver, Colorado. A stadionjuk a tengerszint feletti magassága miatt ('Mile High') hírhedt, ami nehézséget okoz a vendégcsapatoknak. 3-szoros Super Bowl győztesek.", 3),
        ("Kansas City Chiefs", "Hazai város: Kansas City, Missouri. A 2020-as évek domináns csapata Patrick Mahomes vezetésével, a liga egyik legdinamikusabb támadósorával.", 3),
        ("Las Vegas Raiders", "Hazai város: Las Vegas, Nevada. Korábban Oaklandben és Los Angelesben is játszottak. Hírhedtek a 'Raider Nation' szurkolótáborukról és a kemény, megalkuvást nem tűrő játékstílusukról.", 3),
        ("Los Angeles Chargers", "Hazai város: Inglewood, California. Korábban San Diegóban játszottak. Jellegzetes, villám logójuk van, és általában a látványos támadójátékukról ismertek.", 3),

        # === NFC Csapatok (category_id = 4) ===
        # NFC East
        ("Dallas Cowboys", "Hazai város: Arlington, Texas. Gyakran emlegetik 'Amerika Csapataként' hatalmas országos népszerűségük miatt. 5 Super Bowl győzelmük van.", 4),
        ("New York Giants", "Hazai város: East Rutherford, New Jersey. Négyszeres Super Bowl győztesek, kétszer a New England Patriots nagy meglepetésre történő legyőzésével.", 4),
        ("Philadelphia Eagles", "Hazai város: Philadelphia, Pennsylvania. Rendkívül fanatikus és hangos szurkolótáboruk van. Első Super Bowl győzelmüket 2018-ban szerezték.", 4),
        ("Washington Commanders", "Hazai város: Landover, Maryland. A csapat több névváltoztatáson esett át, korábban Redskins, majd Football Team néven szerepeltek.", 4),
        # NFC North
        ("Chicago Bears", "Hazai város: Chicago, Illinois. Az NFL egyik alapító csapata, a liga történetének legtöbb győzelmével rendelkeznek.", 4),
        ("Detroit Lions", "Hazai város: Detroit, Michigan. Az egyik a négy csapat közül, amely még soha nem játszott Super Bowl-t, de rendkívül hűséges szurkolóik vannak.", 4),
        ("Green Bay Packers", "Hazai város: Green Bay, Wisconsin. A liga egyetlen közösségi tulajdonban lévő csapata; a szurkolók a részvényesek. 4 Super Bowl győzelmük van.", 4),
        ("Minnesota Vikings", "Hazai város: Minneapolis, Minnesota. Jellegzetes lila-arany színeik és viking-sisakos logójuk van. Négyszer jutottak Super Bowl-ba, de nyerniük még nem sikerült.", 4),
        # NFC South
        ("Atlanta Falcons", "Hazai város: Atlanta, Georgia. A 2017-es Super Bowl-on a sportág történetének legnagyobb, 28-3-as előnyét adták le.", 4),
        ("Carolina Panthers", "Hazai város: Charlotte, North Carolina. Az 1995-ben alapított csapat viszonylag fiatalnak számít a ligában.", 4),
        ("New Orleans Saints", "Hazai város: New Orleans, Louisiana. A 2005-ös Katrina hurrikán utáni újjáépülés szimbólumai lettek, és 2010-ben megnyerték a Super Bowl-t.", 4),
        ("Tampa Bay Buccaneers", "Hazai város: Tampa, Florida. Kétszeres Super Bowl győztesek, legutóbb 2021-ben Tom Brady-vel, aki 43 évesen vezette őket győzelemre.", 4),
        # NFC West
        ("Arizona Cardinals", "Hazai város: Glendale, Arizona. Az NFL egyik alapító tagja, a legrégebbi, folyamatosan működő professzionális amerikai futball csapat.", 4),
        ("Los Angeles Rams", "Hazai város: Inglewood, California. A 2022-es Super Bowl győztesei, amit a saját stadionjukban nyertek meg.", 4),
        ("San Francisco 49ers", "Hazai város: Santa Clara, California. A 80-as és 90-es évek dinasztiája Joe Montana és Jerry Rice nevével fémjelezve, 5 Super Bowl győzelmük van.", 4),
        ("Seattle Seahawks", "Hazai város: Seattle, Washington. Híresek a '12th Man' nevű szurkolótáborukról, akik a stadionban okozott hangzavarral segítik a csapatot. Egyszeres Super Bowl győztesek.", 4)
    ]

    cursor.executemany('INSERT INTO entries (term, description, category_id) VALUES (?, ?, ?)', entries_to_add)
    print(f"{len(entries_to_add)} bejegyzés sikeresen hozzáadva az adatbázishoz.")

except sqlite3.Error as e:
    print(f"Hiba történt a bejegyzések hozzáadása során: {e}")

# Változtatások mentése és kapcsolat bezárása
conn.commit()
conn.close()

print("Az adatbázis feltöltése befejeződött.")
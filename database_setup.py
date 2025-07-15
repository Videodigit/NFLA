import sqlite3

# Csatlakozás az adatbázishoz (ha nem létezik, létrehozza az nfl_akademia.db fájlt)
conn = sqlite3.connect('nfl_akademia.db')
cursor = conn.cursor()

# --- Táblák létrehozása ---
# Kategóriák tábla (pl: Szabályok, Kifejezések)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
''')

# Bejegyzések tábla (a fogalmak és leírásaik)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT NOT NULL,
        description TEXT NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
''')
print("Adatbázis táblák sikeresen létrehozva.")

# --- Példa adatok feltöltése ---
try:
    categories_to_add = [("Szabályok",), ("Kifejezések",), ("Csapatok (AFC)",)]
    cursor.executemany('INSERT OR IGNORE INTO categories (name) VALUES (?)', categories_to_add)
    
    # Csak akkor töltjük fel a bejegyzéseket, ha még üres a tábla
    cursor.execute("SELECT count(*) FROM entries")
    if cursor.fetchone()[0] == 0:
        entries_to_add = [
            ("Touchdown (TD)", "A támadó csapat pontot szerez, ha a labdát beviszi az ellenfél célterületére (end zone). Értéke 6 pont.", 1),
            ("Field Goal (FG)", "A csapat a labdát a kapuba rúgja. Értéke 3 pont.", 1),
            ("Sack", "Amikor a védelem a labdát birtokló irányítót (quarterback) a kezdővonal mögött a földre viszi.", 2),
            ("Interception", "Amikor egy védőjátékos elkapja az ellenfél irányítójának dobását.", 2),
            ("Buffalo Bills", "Az AFC Keleti divíziójában szereplő csapat, központja Orchard Park, New York.", 3),
            ("Kansas City Chiefs", "Az AFC Nyugati divíziójában szereplő csapat, a 2023-as és 2024-es Super Bowl győztese.", 3)
        ]
        cursor.executemany('INSERT INTO entries (term, description, category_id) VALUES (?, ?, ?)', entries_to_add)
        print("Példa adatok sikeresen hozzáadva.")
    else:
        print("A bejegyzések már léteznek, a feltöltés kihagyva.")

except sqlite3.Error as e:
    print(f"Hiba történt az adatbázis művelet során: {e}")

conn.commit()
conn.close()
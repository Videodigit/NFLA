import sqlite3
from flask import Flask, render_template

# Létrehozzuk a Flask alkalmazás példányt
app = Flask(__name__)

def get_db_connection():
    """
    Létrehoz egy adatbázis-kapcsolatot, amelyen keresztül
    az adatsorokat szótárként (dictionary) lehet elérni.
    """
    conn = sqlite3.connect('nfl_akademia.db')
    # Ez a beállítás teszi lehetővé, hogy a sorokat név alapján érjük el (pl. row['name'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """
    Ez a függvény felel a főoldalért. Lekérdezi az adatokat az adatbázisból,
    átalakítja őket, majd átadja a HTML sablonnak.
    """
    conn = get_db_connection()
    
    # 1. Lekérdezzük az adatokat az adatbázisból.
    #    Az eredmény 'Row' objektumok listája lesz.
    db_categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    db_entries = conn.execute('SELECT * FROM entries ORDER BY term').fetchall()
    
    conn.close()
    
    # 2. ÁTALAKÍTÁS: Ez a kulcsfontosságú lépés, ami a hibát javítja.
    #    A 'Row' objektumok listáját átalakítjuk egyszerű szótárak (dictionary) listájává,
    #    amit a `tojson` filter már képes kezelni.
    categories = [dict(row) for row in db_categories]
    entries = [dict(row) for row in db_entries]
    
    # 3. Átadjuk a már átalakított, tiszta adatokat a HTML sablonnak megjelenítésre.
    return render_template('index.html', categories=categories, entries=entries)

if __name__ == '__main__':
    # Az applikáció futtatása "debug" módban.
    # Ez segít a fejlesztésben, mert hiba esetén részletesebb üzenetet ad.
    app.run(debug=True)
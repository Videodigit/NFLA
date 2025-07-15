import sqlite3
import os  # Ezt a sort hozzáadtuk
from flask import Flask, render_template

app = Flask(__name__)

# ===== ÚJ DEBUG ÚTVONAL KEZDETE =====
@app.route('/debug')
def debug_info():
    """
    Ez egy ideiglenes oldal, ami megmutatja a szerveren lévő fájlokat
    és az adatbázis méretét.
    """
    try:
        path = '.'  # Az aktuális mappa
        files_in_directory = os.listdir(path)
        db_size = f"{os.path.getsize('nfl_akademia.db')} bytes" if 'nfl_akademia.db' in files_in_directory else "Adatbázis nem található."
        
        # HTML válasz építése
        response_html = f"""
        <h1>Szerver Diagnosztika</h1>
        <p><strong>Aktuális mappa:</strong> {os.getcwd()}</p>
        <p><strong>Adatbázis mérete:</strong> {db_size}</p>
        <h2>Fájlok a mappában:</h2>
        <ul>
        """
        for filename in files_in_directory:
            response_html += f"<li>{filename}</li>"
        response_html += "</ul>"
        
        return response_html
    except Exception as e:
        return f"Hiba történt a diagnosztika során: {e}"
# ===== ÚJ DEBUG ÚTVONAL VÉGE =====


def get_db_connection():
    """Létrehoz egy adatbázis-kapcsolatot."""
    conn = sqlite3.connect('nfl_akademia.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """A főoldal, ami lekérdezi az adatokat és megjeleníti őket."""
    conn = get_db_connection()
    categories = [dict(row) for row in conn.execute('SELECT * FROM categories ORDER BY name').fetchall()]
    entries = [dict(row) for row in conn.execute('SELECT * FROM entries ORDER BY term').fetchall()]
    conn.close()
    return render_template('index.html', categories=categories, entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
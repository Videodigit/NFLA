import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    """Létrehoz egy adatbázis-kapcsolatot."""
    conn = sqlite3.connect('nfl_akademia.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """A főoldal, ami lekérdezi és csoportosítja az adatokat a 4 menühöz."""
    conn = get_db_connection()
    
    categories = {row['id']: row['name'] for row in conn.execute('SELECT * FROM categories').fetchall()}
    all_entries = [dict(row) for row in conn.execute('SELECT * FROM entries').fetchall()]
    
    conn.close()

    # Szétválogatjuk a bejegyzéseket a megfelelő listákba
    kifejezesek = [entry for entry in all_entries if categories.get(entry['category_id']) == "Kifejezések"]
    szabalyok = [entry for entry in all_entries if categories.get(entry['category_id']) == "Szabályok"]
    jatekosok = [entry for entry in all_entries if categories.get(entry['category_id']) == "Játékosok"] # ÚJ LISTA
    csapatok = [entry for entry in all_entries if "Csapatok" in categories.get(entry['category_id'], "")]
    
    # A sablonnak átadott adatcsomag
    template_data = {
        "kifejezesek": sorted(kifejezesek, key=lambda x: x['term']),
        "szabalyok": sorted(szabalyok, key=lambda x: x['term']),
        "jatekosok": sorted(jatekosok, key=lambda x: x['term']), # ÚJ LISTA
        "csapatok": sorted(csapatok, key=lambda x: x['term']),
        "all_entries_for_js": all_entries
    }
    
    return render_template('index.html', data=template_data)

if __name__ == '__main__':
    app.run(debug=True)
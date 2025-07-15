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
    """A főoldal, ami lekérdezi és csoportosítja az adatokat a 3 menühöz."""
    conn = get_db_connection()
    
    # Lekérdezzük az összes kategóriát és bejegyzést
    categories = {row['id']: row['name'] for row in conn.execute('SELECT * FROM categories').fetchall()}
    all_entries = [dict(row) for row in conn.execute('SELECT * FROM entries').fetchall()]
    
    conn.close()

    # Szétválogatjuk a bejegyzéseket a megfelelő listákba a kategória neve alapján
    kifejezesek = [entry for entry in all_entries if categories.get(entry['category_id']) == "Kifejezések"]
    szabalyok = [entry for entry in all_entries if categories.get(entry['category_id']) == "Szabályok"]
    csapatok = [entry for entry in all_entries if "Csapatok" in categories.get(entry['category_id'], "")]
    
    # A sablonnak átadott adatcsomag
    # A menük feltöltéséhez a csoportosított listákat, a JS-nek pedig az összeset átadjuk.
    template_data = {
        "kifejezesek": sorted(kifejezesek, key=lambda x: x['term']),
        "szabalyok": sorted(szabalyok, key=lambda x: x['term']),
        "csapatok": sorted(csapatok, key=lambda x: x['term']),
        "all_entries_for_js": all_entries
    }
    
    return render_template('index.html', data=template_data)

if __name__ == '__main__':
    app.run(debug=True)
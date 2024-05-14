from flask import Flask, render_template, request, json
import string
import random
import os
import psycopg2

url_mapping = {}
URL_MAPPINGS_FILE = 'url_mappings.json'

def load_url_mappings():
    print("Loading URL mappings from file:", URL_MAPPINGS_FILE)
    global url_mapping
    try:
        with open(URL_MAPPINGS_FILE, 'r') as f:
            url_mapping = json.load(f)
    except FileNotFoundError:
        pass

app = Flask(__name__)
# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=os.environ.get('DB_HOST'),
    database=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD')
)

# Create a table to store the shortcuts if it doesn't exist
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS shortcuts (
        id SERIAL PRIMARY KEY,
        shortcut TEXT UNIQUE NOT NULL,
        url TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
cur.close()

@app.route('/add', methods=['GET', 'POST'])
def add_url():
    if request.method == 'POST':
        url = request.form['url']
        short_id = generate_short_id()

        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO shortcuts (shortcut, url) VALUES (%s, %s)", (short_id, url))
        except psycopg2.IntegrityError:
            print(f"Error: Shortcut '{short_id}' already exists.")
            return "Error: Shortcut already exists.", 400

        conn.commit()
        cur.close()

        return short_id
    return render_template('add.html')

# Add a route that displays an about page that explains what the app does
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<short_id>')
def redirect_url(short_id):
    if short_id in url_mapping:
        url = url_mapping[short_id] 
        return render_template('view.html', short_id=short_id, url=url)
    else:
        return "URL not found", 404

@app.route('/shortcuts')
def display_shortcuts():
    cur = conn.cursor()
    cur.execute("SELECT shortcut, url, created_at FROM shortcuts ORDER BY created_at DESC")
    shortcuts = cur.fetchall()
    cur.close()
    return render_template('shortcuts.html', shortcuts=shortcuts)

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters+string.digits,k=num_chars))

if __name__ == '__main__':
    load_url_mappings()
    app.run(debug=False)

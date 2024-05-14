from flask import Flask, render_template, request, json, flash, redirect, url_for, make_response
import string
import random
import os
import psycopg2
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')
url_pattern = r'^https?://(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?://(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}'
def is_valid_url(url):
    return bool(re.match(url_pattern, url))

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
        if is_valid_url(url):
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM shortcuts WHERE url = %s", (url,))
            count = cur.fetchone()[0]
            cur.close()

            if count > 0:
                flash('The URL already exists', 'error')
                return redirect(url_for('add_url'))

            # Generate a unique shortcut
            shortcut = generate_short_id()
            while True:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM shortcuts WHERE shortcut = %s", (shortcut,))
                count = cur.fetchone()[0]
                cur.close()
                if count == 0:
                    break
                shortcut = generate_short_id()

            # Save the shortcut and URL to the database
            cur = conn.cursor()
            cur.execute("INSERT INTO shortcuts (shortcut, url) VALUES (%s, %s)", (shortcut, url))
            conn.commit()
            cur.close()

            flash('Shortcut created', 'success')
            return redirect(url_for('add_url'))
        else:
            return "Invalid URL", 400
    return render_template('add.html')

# Add a route that displays an about page that explains what the app does
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<short_id>')
def redirect_url(short_id):
        cur = conn.cursor()
        cur.execute("SELECT url FROM shortcuts WHERE shortcut = %s", (short_id,))
        result = cur.fetchone()
        cur.close()

        if result:
            url = result[0]
            return redirect(url, code=302)
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
    app.run(debug=False)

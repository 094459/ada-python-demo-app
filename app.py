from flask import Flask, render_template, request, json, redirect
import string
import random

app = Flask(__name__)

url_mapping = {}
URL_MAPPINGS_FILE = 'url_mappings.json'

@app.route('/add', methods=['GET', 'POST'])
def add_url():
    if request.method == 'POST':
        url = request.form['url']
        short_id = generate_short_id()
        url_mapping[short_id] = url

        # Load existing mappings from the file
        try:
            with open(URL_MAPPINGS_FILE, 'r') as f:
                url_mappings = json.load(f)
        except FileNotFoundError:
            url_mappings = {}

        # Update the mappings with the new entry
        url_mappings[short_id] = url

        # Write the updated mappings back to the file
        with open(URL_MAPPINGS_FILE, 'w') as f:
            json.dump(url_mappings, f)

        return short_id
    return render_template('add.html')

@app.route('/<short_id>')
def redirect_url(short_id):
    if short_id in url_mapping:
        url = url_mapping[short_id] 
        return render_template('view.html', short_id=short_id, url=url)
    else:
        return "URL not found", 404

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters+string.digits,k=num_chars))

if __name__ == '__main__':
    app.run(debug=True)

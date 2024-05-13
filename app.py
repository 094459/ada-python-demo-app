from flask import Flask, render_template, request, redirect
import string
import random

app = Flask(__name__)

url_mapping = {}

@app.route('/add', methods=['GET', 'POST'])
def add_url():
    if request.methods == 'POST':
        url = request.form['url']
        short_id = generate_short_id()
        url_mapping[short_id] = url
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

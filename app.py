from flask import Flask, render_template, request, redirect
import string
import random

app = Flask(__name__)

url_mapping = {}

# Create a function that returns a random quote that features Yoda
def yoda_quote():
    quotes = [
        "Do. Or do not. There is no try.",
        "I find your lack of faith disturbing.",
        "Do or do not. There is no try.",
        "I am the very model of a modern Major-General.",
        "I've got a bad feeling about this.",
        "Do or do not. There is no try.",
        "I am the very model of a modern Major-General.",
        "I've got a bad feeling about this."]
    return random.choice(quotes)



@app.route('/add', methods=['GET', 'POST'])
def add_url():
    if request.method == 'POST':
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

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', quote=yoda_quote() )

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters+string.digits,k=num_chars))

if __name__ == '__main__':
    app.run(debug=True)

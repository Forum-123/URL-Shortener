import sqlite3
from flask import Flask, jsonify, redirect, render_template, request, url_for
from hashids import Hashids
from werkzeug import exceptions

def connect_to_db():
    connection = sqlite3.connect('shortener/database.db')
    connection.row_factory = sqlite3.Row
    return connection

app = Flask(__name__)
app.config['SECRET_KEY'] = "our-secret-pass"

hashids = Hashids(min_length=5, salt=app.config['SECRET_KEY'])

@app.route('/', methods=['GET', 'POST'])
def home():
    connection = connect_to_db()

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            return redirect(url_for('home'))

        url_query = connection.execute('INSERT INTO URLs (original_url) VALUES (?)', (url,))

        connection.commit()
        connection.close()

        url_id = url_query.lastrowid  # Row id of last modified row
        hash_id = hashids.encode(url_id)  # Make a hash from url_id
        shorten_url = request.host_url + hash_id

        return render_template('home.html', short_url=shorten_url)
    return render_template('home.html', title='Short.io!')

@app.route('/<url_id>', methods=['GET'])
def go_to_original(url_id):
    print(123)
    """Increment clicks value whenever the shortened URL is visited"""
    connection = connect_to_db()

    original_id = hashids.decode(url_id)
    print(original_id)
    print(url_id)
    
    if original_id:
        original_id = original_id[0]
        print(original_id)
        url_query = connection.execute('SELECT original_url, clicks FROM URLs WHERE id = (?)', (original_id,)).fetchone()

        original_url = url_query['original_url']
        clicks = url_query['clicks']

        connection.execute('UPDATE URLs SET clicks = ? WHERE id = ?',
                     (clicks + 1, original_id))

        connection.commit()
        connection.close()
        print(url_id)
        print(original_id)
        print(original_url)
        return redirect(original_url)
    else:
        return redirect(url_for('home'))

@app.route('/stats')
def stats():
    connection = connect_to_db()
    stored_urls = connection.execute('SELECT * FROM URLs').fetchall()
    connection.close()

    urls = []
    for url in stored_urls:
        url = dict(zip(url.keys(), url))

        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)

    return render_template('stats.html', urls=urls)

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return render_template('errors/404.html', title='Oops!'), 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return render_template('errors/500.html', title='Oops!'), 500

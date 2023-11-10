import sqlite3
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for

#create flask application object
app = Flask(__name__)
app.config['SECRET_KEY'] = 's3crEtKey'
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])
#flask view function, return value of index page gets converted into an html response thats sent using app route.
#if request is get, skips the request form and sends user to index.html page.

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))

        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)',
                                (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<id>')
def url_redirect(id):
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        #original id gets value if there is a hashid id
        original_id = hashids.decode(id)
        #Basically checks to see if hashids decoded the id, if it did then redirect, else return invalid 
        if original_id:
            #gets the first value from the tuple
            original_id = original_id[0]

            url_data = conn.execute('SELECT original_url, clicks FROM urls'' WHERE id = (?)',(original_id,)).fetchone()

            original_url=url_data['original_url']
            clicks = url_data['clicks']

            conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',(clicks+1,original_id))

            conn.commit()
            conn.close()
            return redirect(original_url)
        else:
            flash("That url is invalid!")
            return redirect(url_for('index'))
        
@app.route('/stats')
def stats():
     conn = db_connection()

     
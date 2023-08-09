import sqlite3
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for
#creates the database with the schema 
def db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection
#create flask application object
app = Flask(__name__)
app.config['SECRET_KEY'] = "stefanisthebest"
hashids = Hashids(min_length=4,salt=app.config['SECRET_KEY'])
#flask view function, return value of index page gets converted into an html response thats sent using app route.
#if request is get, skips the request form and sends user to index.html page.
@app.route('/',methods = ("GET","POST"))
def index():
    conn = db_connection()
    if request.method == "POST":
        url = request.form['url']
        if not url:
            flash('the url is required!!')
            return redirect(url_for('index'))
        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)',(url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        shorturl = request.host_url +hashid

        return render_template('index.html',shorturl=shorturl)
    return render_template('index.html')


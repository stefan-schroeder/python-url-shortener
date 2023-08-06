import random
import string
from flask import Flask, render_template, redirect, request
app = Flask(__name__)
shortened_urls = {}

def generate_short_url(len=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(len))
    return short_url

@app.route("/", methods= ["GET", "POST"])
def index():
    if request.methods == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        #creates short urls while theyre not in the list
        while short_url in shortened_urls:
            short_url = generate_short_url()
    

        shortened_urls[short_url] = long_url
        return f"Shortened URL: {request.url_root}{short_url}"
    return render_template('index.html')

#redirect short url to originial
@app.route("/", methods = ["GET", "POST"])
def redirect(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "Url not found", 404 
    
if __name__=="__main__":
    app.run(debug=True)

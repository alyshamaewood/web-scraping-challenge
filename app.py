from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape


app = Flask(__name__)

@app.route("/")
def index():
    print("This is where we scrape the data")
    
    return render_template("index.html")



@app.route("/scrape")
def web_scrape():
    print("This is where we scrape the data")

    data = scrape.super_scrape()

    print(data)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
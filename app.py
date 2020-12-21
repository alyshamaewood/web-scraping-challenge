from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():

        mars_data = mongo.db.collection.find_one()

        return render_template("index.html", mars=mars_data)



@app.route("/scrape")
def web_scrape():

    data = scrape.super_scrape()

    mongo.db.collection.update({}, data, upsert=True)


    print(data)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
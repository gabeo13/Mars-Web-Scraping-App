from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/"


@app.route("/")
def index():
    marsFeed = mongo.db.marsFeed.find_one()
    return render_template("index.html", marsFeed=marsFeed)


@ app.route("/scrape")
def scraper():
    marsFeed = mongo.db.marsFeed
    mars_data = scrape_mars.scrape()
    marsFeed.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

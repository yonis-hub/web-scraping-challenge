# Dependencies 
import scrape_mars
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect


# set you flask
app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    scraped_mars_data = mongo.db.scraped_mars_data
    scraped_mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
#     return "Scraping Successful"

if __name__ == "__main__":
    app.run(debug=True)
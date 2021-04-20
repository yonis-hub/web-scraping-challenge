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
    mars_data = mongo.db.mars_data
    mars_results = scrape_mars.scrape()
    # print(f'Printing from scrape line 23 {mars_data}')
    mars_data.update({}, mars_results, upsert=True)
    return redirect("/", code=302 )

if __name__ == "__main__":
    app.run(debug=True)
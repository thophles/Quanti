from flask import Flask, render_template, request
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#always configure app first
app = Flask(__name__)

engine = create_engine("postgresql://theowilliams:Franklin97@localhost/capstone_db")
# # gives each user on the site a personalized session
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
     app.run(debug=True)

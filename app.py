from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from models import db
from functions import GetWord

app = Flask(__name__)
app.config["SECRET_KEY"] = "config_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "se_vocabulary_db")

if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DB_FOLDER, "database.db")}"
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    # get_word = GetWord()
    # get_word.noun()


@app.route("/", methods=["GET", "POST"])
def main_page():
    return render_template("main_page.html")

@app.route("/dictionary", methods=["GET", "POST"])
def dictionary():
    return render_template("dictionary.html")

@app.route("/flashcards", methods=["GET", "POST"])
def flashcards():
    return render_template("flashcards.html")

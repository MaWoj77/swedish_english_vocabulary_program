from routes import blueprint
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from models import db, Noun
from functions import GetWord, GetTranslation

app = Flask(__name__)
app.config["SECRET_KEY"] = "config_secret_key"
app.register_blueprint(blueprint)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "se_vocabulary_db")

if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DB_FOLDER, "database.db")}"
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    if not db.session.query(Noun).all():
        get_word = GetWord()
        get_word.get_word()
    translation = GetTranslation()
    existing_translation = translation.existing_translation()
    if not existing_translation:
        translation.translate()


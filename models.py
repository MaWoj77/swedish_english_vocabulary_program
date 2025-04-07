from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Noun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    noun = db.Column(db.String)
    en_translation = db.Column(db.String)
    indefinite_singular = db.Column(db.String)
    definite_singular = db.Column(db.String)
    indefinite_plural = db.Column(db.String)
    definite_plural = db.Column(db.String)

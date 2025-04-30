from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Noun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baseform = db.Column(db.String)
    en_translation = db.Column(db.String)
    indefinite_singular = db.Column(db.String)
    definite_singular = db.Column(db.String)
    indefinite_plural = db.Column(db.String)
    definite_plural = db.Column(db.String)

class Adjective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baseform = db.Column(db.String)
    en_translation = db.Column(db.String)
    common_singular = db.Column(db.String)
    neuter_singular = db.Column(db.String)
    indefinite_plural = db.Column(db.String)

class Verb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baseform = db.Column(db.String)
    en_translation = db.Column(db.String)
    present = db.Column(db.String)
    preterite = db.Column(db.String)
    supine = db.Column(db.String)
    imperative = db.Column(db.String)

class Adverb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baseform = db.Column(db.String)
    en_translation = db.Column(db.String)

class ProperNoun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baseform = db.Column(db.String)
    en_translation = db.Column(db.String)

class Numeral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baseform = db.Column(db.String)
    en_translation = db.Column(db.String)

class Interjection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baseform = db.Column(db.String)
    en_translation = db.Column(db.String)

class Preposition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baseform = db.Column(db.String)
    en_translation = db.Column(db.String)


# class Expressions(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     expression = db.Column(db.String)
#     en_translation = db.Column(db.String)

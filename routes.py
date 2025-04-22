from flask import Blueprint, request, render_template

blueprint = Blueprint('blueprint', __name__)

@blueprint.route("/", methods=["GET", "POST"])
def main_page():
    return render_template("main_page.html")

@blueprint.route("/dictionary", methods=["GET", "POST"])
def dictionary():
    return render_template("dictionary.html")

@blueprint.route("/flashcards", methods=["GET", "POST"])
def flashcards():
    return render_template("flashcards.html")

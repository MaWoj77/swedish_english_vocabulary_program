from flask import Blueprint, request, render_template, g

blueprint = Blueprint('blueprint', __name__)

@blueprint.route("/", methods=["GET", "POST"])
def main_page():
    return render_template("main_page.html")

@blueprint.route("/dictionary", methods=["GET", "POST"])
def dictionary():
    language = request.form.get("language")
    word_to_translate = str(request.form.get("word_to_translate"))
    g.get_translation.translation(language, word_to_translate)
    return render_template("dictionary.html")

@blueprint.route("/flashcards", methods=["GET", "POST"])
def flashcards():
    return render_template("flashcards.html")

from flask import Blueprint, request, render_template, g

blueprint = Blueprint('blueprint', __name__)

@blueprint.route("/", methods=["GET", "POST"])
def main_page():
    return render_template("main_page.html")

@blueprint.route("/dictionary", methods=["GET", "POST"])
def dictionary():
    data = {}
    if request.method == "POST":
        language = request.form.get("language")
        word_to_translate = str(request.form.get("word_to_translate"))
        data = g.get_translation.translation(language, word_to_translate)
    return render_template("dictionary.html", data=data)

from flask import Blueprint, render_template

display = Blueprint(
    "display",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@display.route("/")
def index():
    return render_template("display/index.html")
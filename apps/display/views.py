from flask import Blueprint, render_template, current_app, jsonify

display = Blueprint(
    "display",
    __name__,
    template_folder="templates",
    static_folder="static",
)

threshold_value = 0.2

@display.route("/")
def index():    
    return render_template("display/index.html", threshold_value=threshold_value)

@display.route("/mastication_count", methods=["GET"])
def get_mastication_count():
    mastication_count = current_app.config['mastication']['count']
    return jsonify({"mastication_count": mastication_count})
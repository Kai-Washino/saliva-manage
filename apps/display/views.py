from flask import Blueprint, render_template, current_app, jsonify
import time

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

@display.route("/is_mastication", methods=["GET"])
def get_is_mastication():    
    now = time.time()
    last_recognized = current_app.config['mastication']["last_recognized"]

    if last_recognized and (now - last_recognized >5):
         current_app.config['mastication']['status'] = False  # 5秒以上経過したらFalseにする

    is_mastication = current_app.config['mastication']['status']

    return jsonify({"is_mastication": is_mastication})
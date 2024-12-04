from flask import Blueprint, render_template, request, jsonify
import requests

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
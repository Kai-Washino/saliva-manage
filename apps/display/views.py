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

@display.route('/buzz', methods=['POST'])
def buzz():
    data = request.get_json()
    m5_ip = data.get('ip')
    if not m5_ip:
        return jsonify({"success": False, "message": "No IP address provided"}), 400

    try:
        response = requests.get(f"http://{m5_ip}/buzz")
        if response.status_code == 200:
            return jsonify({"success": True, "message": "Buzzing"})
        else:
            return jsonify({"success": False, "message": "Failed to buzz"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": str(e)}), 500

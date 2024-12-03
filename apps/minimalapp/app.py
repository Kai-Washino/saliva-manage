from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

receive_count = 0
threshold_value = 0.2

@app.route('/')
def index():
    return render_template('index.html', threshold_value=threshold_value)

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/detect')
def detect():
    return render_template('detect.html', threshold_value=threshold_value)

@app.route('/receive_audio', methods=['POST'])
def receive_audio():
    global receive_count
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_data = request.files['audio']
    # 音声データを受け取ったことを示す処理（ここでは単純にカウントを増やすだけ）
    receive_count += 1
    print(f"Received audio data: {receive_count} times")
    
    # JSON形式でレスポンスを返す
    return jsonify({"message": "Audio received", "count": receive_count})

@app.route('/sound')
def sound():
    return render_template('sound.html')

@app.route('/buzz', methods=['POST'])
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


if __name__ == "__main__":
    app.run(debug=True)

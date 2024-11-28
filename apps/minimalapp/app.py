from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

receive_count = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

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


if __name__ == "__main__":
    app.run(debug=True)

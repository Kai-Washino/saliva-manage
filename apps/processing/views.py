from flask import Blueprint, request, jsonify, current_app

processing = Blueprint(
    "processing",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@processing.route('/receive_audio', methods=['POST'])
def receive_audio():    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_data = request.files['audio']
    # 音声データを受け取ったことを示す処理（ここでは単純にカウントを増やすだけ）
    current_app.config['mastication']['count'] += 1    
    
    # JSON形式でレスポンスを返す
    return jsonify({"message": "Audio received", "count": current_app.config['mastication']['count']})
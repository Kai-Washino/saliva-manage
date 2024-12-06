import os
import numpy as np
import matplotlib.pyplot as plt
from flask import Blueprint, request, jsonify, current_app, send_file, render_template
from services.signal_service import SignalProcessingService
from io import BytesIO
from pathlib import Path
from pydub import AudioSegment
import librosa
import soundfile as sf

processing = Blueprint(
    "processing",
    __name__,
    template_folder="templates",
    static_folder="static",
)

signal_service = SignalProcessingService()

@processing.route('/receive_audio', methods=['POST'])
def receive_audio():    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_data = request.files['audio']
    audio = AudioSegment.from_file(audio_data, format="webm")
    audio_buffer = BytesIO()
    audio.export(audio_buffer, format="wav")
    audio_buffer.seek(0)    

    audio_array, sample_rate = sf.read(audio_buffer)
    normalized_spectrogram = signal_service.stft_audio(audio_array, sample_rate)    
    
    """
    # 音声データやスペクトログラム画像の保存用
    audio_path = save_audio_file(audio_data)
    current_app.config['last_audio_file'] = audio_path
    spectrogram_image_path = generate_spectrogram_image(processed_audio, sample_rate)
    """
    
    # 音声データを受け取ったことを示す処理（ここでは単純にカウントを増やすだけ）
    current_app.config['mastication']['count'] += 1    
    
    # JSON形式でレスポンスを返す
    return jsonify({"message": "Audio received", "count": current_app.config['mastication']['count']}), 200

@processing.route('/stop_measurement', methods=['POST'])
def stop_measurement():   
    current_app.config['mastication']['count'] = 0
    return jsonify({"message": "Audio stopped, mastication count reset"}), 200

@processing.route('/display_audio', methods=['GET'])
def display_audio():
    # 最後に保存された音声ファイルのパスを取得
    audio_path = current_app.config.get('last_audio_file')
    if not audio_path or not Path(audio_path).exists():
        return render_template('processing/no_audio.html')

    # 音声ファイルのパスをテンプレートに渡して表示
    relative_audio_path = Path(audio_path).relative_to(Path('apps/static')).as_posix()
    return render_template('processing/audio.html', audio_path=relative_audio_path)

@processing.route('/display_spectrogram', methods=['GET'])
def display_spectrogram():
    # 最後に生成されたスペクトログラム画像のパスを取得
    image_path = current_app.config.get('last_spectrogram_image')
    if not image_path or not Path(image_path).exists():
        return render_template('processing/no_spectrogram.html')
    
    relative_image_path = Path(image_path).relative_to(Path('apps/static')).as_posix()
    return render_template('processing/spectrogram.html', image_path=relative_image_path)

def save_audio_file(audio_data):
    # 保存するディレクトリを定義
    directory = Path('apps/static/audio')
    # ディレクトリが存在しなければ作成
    directory.mkdir(parents=True, exist_ok=True)
    
    # 音声ファイルを保存
    audio_path = directory / 'last_audio.wav'
    audio_data.save(audio_path)
    return str(audio_path)

def generate_spectrogram_image(processed_audio, sample_rate):
    # スペクトログラムの画像を生成
    plt.figure(figsize=(10, 4))
    plt.specgram(processed_audio, Fs=sample_rate, NFFT=2048, noverlap=1024, cmap='plasma')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram')
    plt.colorbar(label='Intensity (dB)')

    # 画像を保存
    directory = Path('apps/static/images')
    directory.mkdir(parents=True, exist_ok=True)
    image_path = directory / 'spectrogram.png'
    plt.savefig(image_path, format='png')
    plt.close()

    # 保存した画像パスをアプリケーションコンフィグに保持
    current_app.config['last_spectrogram_image'] = image_path

    return image_path
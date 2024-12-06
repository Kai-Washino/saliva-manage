from services.stft_service import STFTService
import librosa
from sklearn.preprocessing import MinMaxScaler

class SignalProcessingService:
    def __init__(self):
        self.scaler = MinMaxScaler()
    
    def stft_audio(self, audio_array, sample_rate):
    # STFTを使ってスペクトログラムを生成
        stft_service = STFTService(sample_rate, audio_array)
        spectrogram = stft_service.generate_spectrogram()

        # スペクトログラムを正規化
        normalized_spectrogram = self.scaler.fit_transform(spectrogram)

        return normalized_spectrogram
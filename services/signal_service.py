from services.stft_service import STFTService
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class SignalProcessingService:
    def __init__(self):
        self.scaler = MinMaxScaler()
    
    def stft_audio(self, audio_array, sample_rate, scale=661, time_range=65):    
        stft_service = STFTService(sample_rate, audio_array)
        spectrogram = stft_service.generate_spectrogram()

        # スペクトログラムを正規化
        normalized_spectrogram = self.scaler.fit_transform(spectrogram)

        # 必要な形にトリミングまたはパディング
        data = self.trim_or_pad(normalized_spectrogram, time_range, scale)

        return data

    def trim_or_pad(self, data, time_range, scale):
        # 現在のスペクトログラムの形状
        current_time_range, current_scale = data.shape
        
        # スケール方向を調整（トリミング/パディング）
        if current_scale > scale:
            data = data[:, :scale]  # スケール方向にトリミング
        elif current_scale < scale:
            padding_scale = scale - current_scale
            data = np.pad(data, ((0, 0), (0, padding_scale)), mode='constant', constant_values=0)
        
        # タイムレンジ方向を調整（トリミング/パディング）
        if current_time_range > time_range:
            data = data[:time_range, :]  # タイムレンジ方向にトリミング
        elif current_time_range < time_range:
            padding_time = time_range - current_time_range
            data = np.pad(data, ((0, padding_time), (0, 0)), mode='constant', constant_values=0)
        
        return data

import numpy as np

from scipy.fftpack import fft

class STFTService:
    def __init__(self, sample_rate, data):
        self.sample_rate = sample_rate
        self.data = data
        self.window_length = int(0.03 * self.sample_rate)
        self.hop_length = int(self.window_length / 2)

    def generate_spectrogram(self):
        # データが複数のチャネルを持つ場合は平均を取る
        if len(self.data.shape) > 1:
            self.data = self.data.mean(axis=1)
        
        # スペクトログラムを格納するリスト
        spectrogram = []
        
        # ウィンドウごとにFFTを実行
        for start in range(0, len(self.data) - self.window_length, self.hop_length):
            windowed_data = self.data[start:start + self.window_length]
            Y = fft(windowed_data)
            power = np.abs(Y[:int(self.window_length / 2)])**2
            spectrogram.append(power)
        
        self.spectrogram = np.array(spectrogram).T
        if type(self.spectrogram) == tuple:
            self.spectrogram = np.abs(self.spectrogram)   

        if self.spectrogram.ndim == 1:
            self.spectrogram = spectrogram.reshape(-1, 1)     
                    
        return  self.spectrogram
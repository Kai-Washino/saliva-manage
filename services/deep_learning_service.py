import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Masking

class DeepLearningService:
    def __init__(self, model_path):
        self.model = load_model(model_path, custom_objects={'Masking': Masking})
        # self.model = load_model(model_path)

    def predict(self, input_data):
        return self.model.predict(input_data)


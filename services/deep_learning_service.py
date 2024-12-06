import numpy as np

from models.model_loader import load_trained_model

class DeepLearningService:
    def __init__(self, model_path):
        self.model = load_trained_model(model_path)

    def predict(self, input_data):
        return self.model.predict(input_data)

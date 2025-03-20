import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from PIL import Image
import os

class MushroomModel:
    def __init__(self, model_path=None):
        self.model = self.load_model(model_path)
        
    def load_model(self, model_path=None):
        if model_path and os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
        else:
            model = ResNet50(weights='imagenet')
        return model
    
    def save_model(self, path='mushroom_model'):
        if not os.path.exists(path):
            os.makedirs(path)
        self.model.save(f'{path}/model.h5')
        return f'{path}/model.h5'
    
    def preprocess_image(self, img):
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array
    
    def predict(self, img):
        img_array = self.preprocess_image(img)
        predictions = self.model.predict(img_array)
        results = decode_predictions(predictions, top=5)[0]
        return results 
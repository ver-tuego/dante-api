import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from scipy.spatial.distance import cosine
base_model = ResNet50(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)


def load_and_process_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array


def get_image_features(image_path):
    img = load_and_process_image(image_path)
    features = model.predict(img)
    return features.flatten()


def compare_images(image_path1, image_path2):
    features1 = get_image_features(image_path1)
    features2 = get_image_features(image_path2)
    similarity = 1 - cosine(features1, features2)
    return similarity > 0.75
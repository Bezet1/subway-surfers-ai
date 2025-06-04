import os

DATA_DIR = os.path.join("screen_collector", "screens")

MODEL_PATH = os.path.join("trained_models", "best_model.h5")

# Kolejność alfabetyczna - tak jak TensorFlow ładuje klasy domyślnie
CLASS_NAMES = ['DOWN', 'LEFT', 'NONE', 'RIGHT', 'UP']

SAMPLE_IMAGE_PATH = os.path.join("screen_collector", "screens", "DOWN", "test.png")
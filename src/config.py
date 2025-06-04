import os

DATA_DIR = os.path.join("screen_collector", "screens")
MODEL_PATH = os.path.join("trained_models", "best_model.h5")
CLASS_NAMES = ['DOWN', 'LEFT', 'NONE', 'RIGHT', 'UP']
SAMPLE_IMAGE_PATH = os.path.join("screen_collector", "screens", "DOWN", "test.png")

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
LEARNING_RATE = 0.0001 
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1
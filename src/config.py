import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join("screen_collector", "screens")

# Speed-specific paths
SLOW_DATA_DIR = os.path.join(DATA_DIR, "slow")
MEDIUM_DATA_DIR = os.path.join(DATA_DIR, "medium")
FAST_DATA_DIR = os.path.join(DATA_DIR, "fast")

# Model paths for each speed category
MODELS_DIR = os.path.join("trained_models")
SLOW_MODEL_PATH = os.path.join(MODELS_DIR, "slow_model.h5")
MEDIUM_MODEL_PATH = os.path.join(MODELS_DIR, "medium_model.h5")
FAST_MODEL_PATH = os.path.join(MODELS_DIR, "fast_model.h5")

# Class names remain the same for all models
CLASS_NAMES = ['DOWN', 'LEFT', 'NONE', 'RIGHT', 'UP']

# Sample image path
SAMPLE_IMAGE_PATH = os.path.join(DATA_DIR, "slow", "DOWN", "test.png")

# Training parameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
LEARNING_RATE = 0.0001 
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1
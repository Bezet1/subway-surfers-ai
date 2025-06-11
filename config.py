import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join("screen_collector", "screens")

# Speed folder names
SLOW_FOLDER = 'slow'
MEDIUM_FOLDER = 'medium'
FAST_FOLDER = 'fast'

SPEED_CATEGORIES = [SLOW_FOLDER, MEDIUM_FOLDER, FAST_FOLDER]

# Speed-specific paths
SLOW_DATA_DIR = os.path.join(DATA_DIR, SLOW_FOLDER)
MEDIUM_DATA_DIR = os.path.join(DATA_DIR, MEDIUM_FOLDER)
FAST_DATA_DIR = os.path.join(DATA_DIR, FAST_FOLDER)

# Model paths for each speed category
MODELS_DIR = os.path.join("trained_models")
SLOW_MODEL_PATH = os.path.join(MODELS_DIR, "slow_model.keras")
MEDIUM_MODEL_PATH = os.path.join(MODELS_DIR, "medium_model.h5")
FAST_MODEL_PATH = os.path.join(MODELS_DIR, "fast_model.keras")

DOWN = 'DOWN'
LEFT = 'LEFT'
NONE = 'NONE'
RIGHT = 'RIGHT'
UP = 'UP'

# Class names remain the same for all models
CLASS_NAMES = [DOWN, LEFT, NONE, RIGHT, UP]

# Sample image path
SAMPLE_IMAGE_PATH = os.path.join(DATA_DIR, SLOW_FOLDER, DOWN, "test.png")

# Training parameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
LEARNING_RATE = 0.0001 
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1

# Speed timer thresholds
SLOW_THRESHOLD = 30 
MEDIUM_THRESHOLD = 120  

#Bot configuration
SLOW_DELAY = 0.4
MEDIUM_DELAY = 0.3
FAST_DELAY = 0.1

PRECISION_THRESHOLD = 0.60
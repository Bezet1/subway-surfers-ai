import os

# Ścieżka do katalogu z obrazami treningowymi
DATA_DIR = os.path.join("screen-collector", "screens")

# Ścieżka do zapisanego (wytrenowanego) modelu
MODEL_PATH = os.path.join("trained_models", "best_model.h5")

# Nazwy klas odpowiadające kierunkom ruchu w grze
CLASS_NAMES = ['DOWN', 'LEFT', 'RIGHT', 'UP']

# Przykładowy obraz do przewidywania (do testów)
SAMPLE_IMAGE_PATH = os.path.join("screen-collector", "screens", "DOWN", "example2.png")

import tensorflow as tf
import os
import numpy as np
from src.data_loader import load_data
from src.model_builder import build_model
from src.trainer import train_model
from src.evaluator import evaluate_model
from utils.predict import predict_image
from utils.plot_metrics import plot_training_metrics
from src.config import DATA_DIR, MODEL_PATH, CLASS_NAMES, SAMPLE_IMAGE_PATH

# Sprawdzanie równowagi klas
def check_class_balance(data_dir):
    class_counts = {}
    for class_name in os.listdir(data_dir):
        class_path = os.path.join(data_dir, class_name)
        if os.path.isdir(class_path):
            class_counts[class_name] = len(os.listdir(class_path))
    
    print("\nDystrybucja klas:")
    for class_name, count in class_counts.items():
        print(f"{class_name}: {count} obrazów")
    
    # Sprawdź, czy klasy są zbalansowane
    counts = list(class_counts.values())
    imbalance_ratio = max(counts) / min(counts) if min(counts) > 0 else float('inf')
    print(f"Współczynnik niezbalansowania: {imbalance_ratio:.2f}")
    
    return class_counts, imbalance_ratio

# Sprawdź równowagę klas
class_counts, imbalance_ratio = check_class_balance(DATA_DIR)

# Ładowanie danych
data, class_names = load_data(DATA_DIR, img_size=(256, 256), batch_size=32)
default_class_names = class_names

# Podział danych na zbiory treningowy, walidacyjny i testowy
train_size = int(0.7 * len(data))
val_size = int(0.2 * len(data))
test_size = len(data) - train_size - val_size

train_data = data.take(train_size)
val_data = data.skip(train_size).take(val_size)
test_data = data.skip(train_size + val_size)

print(f"\n\nDataset split:")
print(f"Total samples:     {len(data)}")
print(f"Training samples:  {train_size}")
print(f"Validation samples:{val_size}")
print(f"Test samples:      {test_size}")

print("\n\nTraining new model...")
model = build_model(num_classes=len(default_class_names))
print(model.summary())

history = train_model(model, train_data, val_data, MODEL_PATH)
plot_training_metrics(history)

metrics = evaluate_model(model, test_data)
print(f"\n\nPrecision: {metrics['precision']:.4f}")
print(f"Recall: {metrics['recall']:.4f}")
print(f"Accuracy: {metrics['accuracy']:.4f}")

# Sprawdź, czy model ma problemy z konkretnymi klasami
print("\nTestowanie modelu na próbkach z poszczególnych klas:")

# Funkcja do ewaluacji modelu na poszczególnych klasach
def evaluate_per_class(model, data_dir, class_names, img_size=(256, 256)):
    results = {}
    
    for i, class_name in enumerate(class_names):
        class_path = os.path.join(data_dir, class_name)
        correct = 0
        total = 0
        
        # Sprawdź tylko pierwsze 20 obrazów z każdej klasy, żeby nie zajęło to zbyt dużo czasu
        files = os.listdir(class_path)[:20]
        
        for file in files:
            if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            file_path = os.path.join(class_path, file)
            try:
                img = tf.keras.preprocessing.image.load_img(file_path, target_size=img_size)
                img_array = tf.keras.preprocessing.image.img_to_array(img)
                
                predicted_class, confidence = predict_image(model, img_array, class_names=class_names)
                
                if predicted_class == class_name:
                    correct += 1
                total += 1
                
            except Exception as e:
                print(f"Błąd przy przetwarzaniu {file_path}: {e}")
        
        accuracy = correct / total if total > 0 else 0
        results[class_name] = {'accuracy': accuracy, 'total': total, 'correct': correct}
        print(f"Klasa {class_name}: dokładność {accuracy:.2f} ({correct}/{total})")
    
    return results

class_results = evaluate_per_class(model, DATA_DIR, default_class_names)
print("\n")
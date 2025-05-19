import tensorflow as tf
import os
from src.data_loader import load_data
from src.model_builder import build_model
from src.trainer import train_model
from src.evaluator import evaluate_model
from utils.predict import predict_image
from utils.plot_metrics import plot_training_metrics
from src.config import DATA_DIR, MODEL_PATH, CLASS_NAMES, SAMPLE_IMAGE_PATH
import cv2

data, class_names = load_data(DATA_DIR, img_size=(256, 256), batch_size=32)
default_class_names = class_names
train_size = int(0.7 * len(data))
val_size = int(0.2 * len(data)) + 1
test_size = int(0.1 * len(data)) + 1
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
history = train_model(model, train_data, val_data, MODEL_PATH)
plot_training_metrics(history)

metrics = evaluate_model(model, test_data)
print(f"\n\nPrecision: {metrics['precision']:.4f}")
print(f"Recall: {metrics['recall']:.4f}")
print(f"Accuracy: {metrics['accuracy']:.4f}")
print("\n")
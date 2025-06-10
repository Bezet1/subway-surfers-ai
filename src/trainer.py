import os
from tensorflow.keras.callbacks import (ModelCheckpoint, TensorBoard, EarlyStopping, 
                                      ReduceLROnPlateau, CSVLogger)
from sklearn.utils import class_weight
import numpy as np
from config import CLASS_NAMES

def calculate_class_weights(train_data):
  y_true = []
  
  for _, labels_batch in train_data:
    y_true.extend(np.argmax(labels_batch.numpy(), axis=1))
  
  y_true = np.array(y_true)
  
  unique, counts = np.unique(y_true, return_counts=True)
  print("Rozkład klas w danych treningowych:")
  for class_idx, count in zip(unique, counts):
    print(f"  {CLASS_NAMES[class_idx]}: {count} próbek")
  
  class_weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=unique,
    y=y_true
  )
  
  class_weight_dict = dict(zip(unique, class_weights))
  print("Wagi klas:", class_weight_dict)
  
  return class_weight_dict

def train_model(model, train_data, val_data, model_path, 
                        logdir='logs', epochs=50, patience=10):
    
  os.makedirs(os.path.dirname(model_path), exist_ok=True)
  os.makedirs(logdir, exist_ok=True)
  
  class_weights = calculate_class_weights(train_data)
  
  callbacks = [
    ModelCheckpoint(
      filepath=model_path,
      save_best_only=True,
      monitor='val_accuracy',
      mode='max',
      verbose=1,
      save_weights_only=False
    ),  
    TensorBoard(
      log_dir=logdir,
      histogram_freq=1,
      write_graph=True,
      write_images=True
    ),
    EarlyStopping(
      monitor='val_accuracy',
      patience=patience,
      restore_best_weights=True,
      verbose=1
    ),
    ReduceLROnPlateau(
      monitor='val_loss',
      factor=0.5,
      patience=5,
      min_lr=1e-7,
      verbose=1
    ),
    
    CSVLogger(
      os.path.join(logdir, 'training_log.csv'),
      append=True
    )
  ]
  
  print("Rozpoczynam trening...")
  print(f"Epochy: {epochs}")
  print(f"Wagi klas: {class_weights}")
  
  history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=epochs,
    callbacks=callbacks,
    class_weight=class_weights,
    verbose=1
  )
  
  return history
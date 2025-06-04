import os
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard, EarlyStopping, ReduceLROnPlateau

def train_model(model, train_data, val_data, model_path, logdir='logs', epochs=30):
  os.makedirs(os.path.dirname(model_path), exist_ok=True)
  
  # TensorBoard do monitorowania procesu uczenia
  tensorboard_callback = TensorBoard(log_dir=logdir)
  
  # Zapisywanie najlepszego modelu na podstawie val_loss
  checkpoint_cb = ModelCheckpoint(
    filepath=model_path,
    save_best_only=True,
    monitor="val_loss",
    verbose=1
  )
  
  # Early stopping - zatrzymanie treningu, gdy model przestaje się poprawiać
  early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,           # Liczba epok bez poprawy, po której trening zostanie zatrzymany
    restore_best_weights=True,
    verbose=1
  )
  
  # Redukcja learning rate, gdy model przestaje się poprawiać
  reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,            # Zmniejsz learning rate o 80%
    patience=3,            # Po 3 epokach bez poprawy
    min_lr=0.00001,        # Minimalny learning rate
    verbose=1
  )
  
  # Trening modelu z wszystkimi callbackami
  history = model.fit(
    train_data, 
    epochs=epochs, 
    validation_data=val_data, 
    callbacks=[
      tensorboard_callback, 
      checkpoint_cb, 
      early_stopping, 
      reduce_lr
    ]
  )
  
  return history
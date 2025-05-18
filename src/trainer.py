import os
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard

def train_model(model, train_data, val_data, model_path, logdir='logs', epochs=20):
  os.makedirs(os.path.dirname(model_path), exist_ok=True)
  tensorboard_callback = TensorBoard(log_dir=logdir)

  checkpoint_cb = ModelCheckpoint(
    filepath=model_path,  # where to save
    save_best_only=True,  # only save best based on val_loss
    monitor="val_loss",                 
    verbose=1
  )

  history = model.fit(
    train_data, 
    epochs=epochs, 
    validation_data=val_data, 
    callbacks=[tensorboard_callback, checkpoint_cb]
  )
  return history
import tensorflow as tf
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.metrics import Precision, Recall, CategoricalAccuracy
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from tensorflow.keras.losses import CategoricalCrossentropy
import matplotlib.pyplot as plt
import sys
import cv2

data_dir = os.path.join("..", "screen-collector", "screeny")
trained_model_path = "trained_models/best_model.h5"

def model_prediction(model, class_names = ["DOWN", "LEFT", "RIGHT", "UP"]):
  img_down_path = "../screen-collector/screeny/DOWN/example.png"
  img_up_path = "../screen-collector/screeny/UP/example.png"
  img_left_path = "../screen-collector/screeny/LEFT/example.png"
  img_right_path = "../screen-collector/screeny/RIGHT/example.png"

  img = cv2.cvtColor(cv2.imread(img_left_path), cv2.COLOR_BGR2RGB)
  resize = tf.image.resize(img, (256, 256))

  prediction = model.predict(tf.expand_dims(resize/255, 0))

  predicted_class_index = prediction.argmax()  # Get the index with the highest probability
  predicted_class_name = class_names[predicted_class_index]

  print(f"Predicted class: {predicted_class_name}")
  print(f"Confidence: {prediction[0][predicted_class_index]:.2f}")

if os.path.exists(trained_model_path):
    print("✅ Model found. Loading existing model...")
    model = tf.keras.models.load_model(trained_model_path)  
    model_prediction(model)

else:
  gpus = tf.config.experimental.list_physical_devices('GPU')
  for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)

  print("Keras dataset: ", tf.keras.utils.image_dataset_from_directory)

  ######## Load image dataset ########
  data = tf.keras.utils.image_dataset_from_directory(
      data_dir,
      label_mode='categorical',       # one-hot labels
      image_size=(256, 256),          # resize all images
      batch_size=32
  )

  data_iterator = data.as_numpy_iterator()
  batch = data_iterator.next()
  class_names = data.class_names

  print("Class names:", class_names)
  print("Batch shape:", batch[0].shape)  # Images
  print("Labels shape:", batch[1].shape)  # One-hot labels
  print("Label example:", batch[1][0])

  fig, ax = plt.subplots(ncols=4, figsize=(20, 20))
  for idx, img in enumerate(batch[0][:4]):
      label_idx = batch[1][idx].argmax()
      class_name = class_names[label_idx]
      ax[idx].imshow(img.astype("uint8"))
      ax[idx].set_title(class_name)
  plt.show()

  data = data.map(lambda x, y: (x/255, y))

  data = data.cache().shuffle(1000)
  train_size = int(0.7 * len(data))
  val_size = int(0.2 * len(data)) + 1
  test_size = int(0.1 * len(data)) + 1

  print("data123", len(data), train_size, val_size, test_size)

  ######## Model ########
  train = data.take(train_size)
  val = data.skip(train_size).take(val_size)
  test = data.skip(train_size + val_size)

  model = Sequential()
  model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)))
  model.add(MaxPooling2D())

  model.add(Conv2D(32, (3, 3), activation='relu'))
  model.add(MaxPooling2D())

  model.add(Conv2D(16, (3, 3), activation='relu'))
  model.add(MaxPooling2D())

  model.add(Flatten())

  model.add(Dense(256, activation='relu'))
  model.add(Dense(4, activation='softmax'))

  model.compile(optimizer='adam',loss=CategoricalCrossentropy(), metrics=['accuracy'])

  ######## Training ########
  logdir='logs'
  os.makedirs(os.path.dirname(trained_model_path), exist_ok=True)
  tensorboard_callback = TensorBoard(log_dir=logdir)

  checkpoint_cb = ModelCheckpoint(
    filepath=trained_model_path,  # where to save
    save_best_only=True,                 # only save best based on val_loss
    monitor="val_loss",                 
    verbose=1
  )
  
  hist = model.fit(
    train, 
    epochs=20, 
    validation_data=val, 
    callbacks=[tensorboard_callback, checkpoint_cb]
  )

  fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))

  # Plot Loss
  ax1.plot(hist.history['loss'], color='blue', label='loss')
  ax1.plot(hist.history['val_loss'], color='orange', label='val_loss')
  ax1.set_title('Loss')
  ax1.set_xlabel('Epoch')
  ax1.set_ylabel('Loss')
  ax1.legend(loc='upper right')

  # Plot Accuracy
  ax2.plot(hist.history['accuracy'], color='green', label='accuracy')
  ax2.plot(hist.history['val_accuracy'], color='red', label='val_accuracy')
  ax2.set_title('Accuracy')
  ax2.set_xlabel('Epoch')
  ax2.set_ylabel('Accuracy')
  ax2.legend(loc='lower right')

  fig.suptitle('Training Metrics', fontsize=16)
  plt.tight_layout()
  plt.show()

  ######## Evaluation ########
  pre = Precision()
  rec = Recall()
  acc = CategoricalAccuracy()

  for batch in test.as_numpy_iterator():
      x, y = batch
      y_pred = model.predict(x)
      pre.update_state(y, y_pred)
      rec.update_state(y, y_pred)
      acc.update_state(y, y_pred)

  print(f"Precision: {pre.result().numpy():.4f}")
  print(f"Recall: {rec.result().numpy():.4f}")
  print(f"Accuracy: {acc.result().numpy():.4f}")
  
  ######## Prediction ########
  model_prediction(model, class_names)



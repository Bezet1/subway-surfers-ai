from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.losses import CategoricalCrossentropy

def build_model(input_shape=(256, 256, 3), num_classes=4):
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

  return model
import tensorflow as tf
from src.config import *
def predict_image(model, img, class_names = ["DOWN", "LEFT", "RIGHT", "UP"]):
  resize = tf.image.resize(img, IMG_SIZE)

  prediction = model.predict(tf.expand_dims(resize/255, 0))

  predicted_class_index = prediction.argmax()  # Get the index with the highest probability
  predicted_class_name = CLASS_NAMES[predicted_class_index]
  confidence = prediction[0][predicted_class_index]
  
  return predicted_class_name, confidence
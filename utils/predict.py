import tensorflow as tf
import cv2

def predict_image(model, img, class_names = ["DOWN", "LEFT", "RIGHT", "UP"]):
  resize = tf.image.resize(img, (256, 256))

  prediction = model.predict(tf.expand_dims(resize/255, 0))

  predicted_class_index = prediction.argmax()  # Get the index with the highest probability
  predicted_class_name = class_names[predicted_class_index]
  confidence = prediction[0][predicted_class_index]
  
  return predicted_class_name, confidence
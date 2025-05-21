from src.config import DATA_DIR, MODEL_PATH, CLASS_NAMES, SAMPLE_IMAGE_PATH
import tensorflow as tf
import os
from screen_collector.src.screen_selector import select_screen_area
import keyboard
import time
from PIL import ImageGrab
from utils.predict import predict_image

DELAY = 0.5
precision_threshold = 0.99
paused = False

if not os.path.exists(MODEL_PATH):
  print("\nModel not found. Quit...")
  exit()

print("\nModel found. Loading existing model...")
model = tf.keras.models.load_model(MODEL_PATH)
selection_area = select_screen_area()

if not selection_area:
  print("No screen area selected. Quit...")
  exit()

while True:
  if keyboard.is_pressed('space'):
    paused = not paused
    print("Program PAUSED. Press Space to resume." if paused else "Program RESUMED.")
    time.sleep(0.3)

  if paused:
    time.sleep(0.1)
    continue

  try:
    snapshot = ImageGrab.grab(bbox=selection_area)
    predicted_class, confidence = predict_image(model, snapshot)
  except Exception as e:
    print(f"Error during prediction: {e}")
    time.sleep(DELAY)
    continue
  
  print(f"\nPredicted class: {predicted_class}, confidence: {confidence:.2f}")
  if confidence > precision_threshold:
    if predicted_class == "LEFT":
      print("\nLEFT")
      keyboard.press_and_release('left')
    elif predicted_class == "RIGHT":
      print("\nRIGHT")
      keyboard.press_and_release('right')
    elif predicted_class == "UP":
      print("\nUP")
      keyboard.press_and_release('up')
    elif predicted_class == "DOWN":
      print("\nDOWN")
      keyboard.press_and_release('down')
    elif predicted_class == "NONE":
      print("\nNONE - No action needed")

  time.sleep(DELAY)

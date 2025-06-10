from config import *
import tensorflow as tf
import os
from screen_collector.src.screen_selector import select_screen_area
import keyboard
import time
from PIL import ImageGrab
from utils.predict import predict_image
from utils.get_speed_category import get_speed_category

paused = False

# Timer variables
start_time = time.time()
elapsed_time = 0

# Check if models exist
if not (os.path.exists(SLOW_MODEL_PATH) and 
        os.path.exists(MEDIUM_MODEL_PATH) and 
        os.path.exists(FAST_MODEL_PATH)):
    print("\nOne or more models not found. Please train the models first.")
    exit()

print("\nLoading models...")
slow_model = tf.keras.models.load_model(SLOW_MODEL_PATH)
medium_model = tf.keras.models.load_model(MEDIUM_MODEL_PATH)
fast_model = tf.keras.models.load_model(FAST_MODEL_PATH)
print("All models loaded successfully.")

selection_area = select_screen_area()

if not selection_area:
    print("No screen area selected. Quit...")
    exit()

# Function to get the appropriate model based on speed category
def get_model_for_speed(speed_category):
    if speed_category == SLOW_FOLDER:
        return slow_model
    elif speed_category == MEDIUM_FOLDER:
        return medium_model
    else:  # fast
        return fast_model
    
def get_delay_for_speed(speed_category):
    if speed_category == SLOW_FOLDER:
        return SLOW_DELAY
    elif speed_category == MEDIUM_FOLDER:
        return MEDIUM_DELAY
    else:
        return FAST_DELAY

print("Bot started. Press space to pause/resume. Press r to reset timer.")

while True:
    if not paused:
        current_time = time.time()
        elapsed_time = current_time - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        speed_category = get_speed_category(elapsed_time)
        delay = get_delay_for_speed(elapsed_time)

        print(f"\rElapsed time: {minutes:02d}:{seconds:02d} - Using {speed_category} model", end="")
    
    if keyboard.is_pressed('space'):
        paused = not paused
        print("\nProgram PAUSED. Press Space to resume." if paused else "\nProgram RESUMED.")
        time.sleep(0.3)

    if keyboard.is_pressed('r'):
        start_time = time.time()
        elapsed_time = 0
        print("\nTimer reset!")
        time.sleep(0.3)

    if paused:
        time.sleep(0.1)
        continue

    try:
        snapshot = ImageGrab.grab(bbox=selection_area)
        speed_category = get_speed_category(elapsed_time)
        current_model = get_model_for_speed(speed_category)
        
        # Predict using the appropriate model
        predicted_class, confidence = predict_image(current_model, snapshot)
        
    except Exception as e:
        print(f"\nError during prediction: {e}")
        time.sleep(delay)
        continue
    
    print(f"\nPredicted class: {predicted_class}, confidence: {confidence:.2f}, using {speed_category} model")
    
    if confidence >= PRECISION_THRESHOLD:
        if predicted_class == LEFT:
            print("\nLEFT")
            keyboard.press_and_release('left')
        elif predicted_class == RIGHT:
            print("\nRIGHT")
            keyboard.press_and_release('right')
        elif predicted_class == UP:
            print("\nUP")
            keyboard.press_and_release('up')
        elif predicted_class == DOWN:
            print("\nDOWN")
            keyboard.press_and_release('down')
        elif predicted_class == NONE:
            print("\nNONE - No action needed")

    time.sleep(delay)
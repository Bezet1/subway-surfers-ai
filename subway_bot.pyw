from config import *
import tensorflow as tf
import os
from screen_collector.src.screen_selector import select_screen_area
import keyboard
import time
from PIL import ImageGrab
from utils.predict import predict_image
from utils.get_speed_category import get_speed_category
import tkinter as tk
from tkinter import ttk
import threading
import pyautogui


paused = True
enabled = False
 # Timer variables
start_time = time.time()
elapsed_time = 0

# Lane tracking variable
lane = 0

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

# Create GUI window
root = tk.Tk()
root.title("Subway Surfers AI Bot")
root.geometry("400x60")
root.resizable(False, False)

# Position window below selected area
if selection_area:
    window_x = selection_area[0]
    window_y = selection_area[3] + 10  # 10 pixels below bottom of selected area
    root.geometry(f"400x60+{window_x}+{window_y}")

# Button functions
def toggle_pause():
    global paused
    paused = not paused
    pause_btn.config(text="Resume" if paused else "Pause")

def reset_timer():
    global start_time, elapsed_time, lane
    start_time = time.time()
    elapsed_time = 0
    lane = 0
    print("\nTimer reset!")
def double_click():
    global enabled
    enabled = not enabled
    doubleclick_btn.config(text="Disable DC" if enabled else "Enable DC")
def double_click_loop():
    while True:
        if enabled:
            pyautogui.click(clicks=2, interval=0.1)
        time.sleep(3)



# Create GUI elements
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

pause_btn = ttk.Button(frame, text="Resume", command=toggle_pause)
pause_btn.grid(row=0, column=0, padx=5)

reset_btn = ttk.Button(frame, text="Reset", command=reset_timer)
reset_btn.grid(row=0, column=1, padx=5)

doubleclick_btn = ttk.Button(frame, text="Enable DC", command=double_click)
doubleclick_btn.grid(row=0, column=2, padx=5)

# Configure grid weights
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Function to get the appropriate model based on speed category
def get_model_for_speed(speed_category):
    if speed_category == SLOW_FOLDER:
        return slow_model
    elif speed_category == MEDIUM_FOLDER:
        return medium_model
    else:
        return fast_model
    
def get_delay_for_speed(elapsed_seconds):
    if elapsed_seconds < SLOW_THRESHOLD:
        return SLOW_DELAY
    elif elapsed_seconds < MEDIUM_THRESHOLD:
        return MEDIUM_DELAY
    else:
        return FAST_DELAY

def current_line():
    if lane == 0:
        return "middle"
    elif lane == -1:
        return "left"
    elif lane == 1:
        return "right"
    else:
        return "cos sie ostro zepsulo"

print("Bot started. Press space to pause/resume. Press r to reset timer.")

def bot_loop():
    global lane
    while True:
        # Calculate delay at the beginning of each loop
        current_time = time.time()
        elapsed_time = current_time - start_time
        speed_category = get_speed_category(elapsed_time)
        delay = get_delay_for_speed(elapsed_time)
        
        if not paused:
            minutes, seconds = divmod(int(elapsed_time), 60)
            print(f"\rElapsed time: {minutes:02d}:{seconds:02d} - Using {speed_category} model", end="")
        
        # Handle keyboard input
        if keyboard.is_pressed('space'):
            toggle_pause()
            time.sleep(0.3)

        if keyboard.is_pressed('r'):
            reset_timer()
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

        print(f"\nPredicted class: {predicted_class}, confidence: {confidence:.2f}, using {speed_category} model, probable line {current_line()}")

        if confidence >= PRECISION_THRESHOLD:
            if predicted_class == LEFT: 
                print("\nLEFT")
                lane -= 1
                lane = max(lane, -1)
                keyboard.press_and_release('left')
            elif predicted_class == RIGHT:  
                print("\nRIGHT")
                lane += 1
                lane = min(lane, 1)
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

# Start bot in separate thread
bot_thread = threading.Thread(target=bot_loop, daemon=True)
bot_thread.start()
dc_thread = threading.Thread(target=double_click_loop, daemon=True)
dc_thread.start()

# Start GUI
root.mainloop()
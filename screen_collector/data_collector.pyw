import os
from PIL import ImageGrab, Image
import keyboard
import time
import datetime
import tkinter as tk
from tkinter import messagebox
import pyautogui  
from src.screen_selector import select_screen_area

# Base screens path
base_screens_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screens')
paused = False
selection_area = None

# Timer variables
start_time = time.time()
elapsed_time = 0

# Create speed category folders
speed_categories = ["slow", "medium", "fast"]
for category in speed_categories:
    category_path = os.path.join(base_screens_path, category)
    os.makedirs(category_path, exist_ok=True)
    print(f"Speed category directory '{category}' ready.")
    
    # Create action folders within each speed category
    action_classes = ["LEFT", "RIGHT", "UP", "DOWN", "NONE"]
    for action in action_classes:
        action_path = os.path.join(category_path, action)
        os.makedirs(action_path, exist_ok=True)
        print(f"  Action directory '{action}' in '{category}' ready.")

# Ask user to select screen area
print("Please select the area of the screen you want to capture.")
selection_area = select_screen_area()

if selection_area:
    print(f"Selected area: {selection_area}")
    print("Program started. Press arrow keys or WASD to take screenshots.")
    print("Press Space to pause/resume. Press r to reset timer. Press Shift+Esc to exit.")
else:
    print("No area selected. Using full screen capture.")

# Function to get time category based on elapsed time
def get_speed_category(elapsed_seconds):
    if elapsed_seconds < 90:  # 0 to 1:30 minutes
        return "slow"
    elif elapsed_seconds < 150:  # 1:30 to 2:30 minutes
        return "medium"
    else:  # 2:30+ minutes
        return "fast"

# Main loop
while True:
    if not paused:
        current_time = time.time()
        elapsed_time = current_time - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        speed_category = get_speed_category(elapsed_time)
        print(f"\rElapsed time: {minutes:02d}:{seconds:02d} - Category: {speed_category}", end="")
    
    if keyboard.is_pressed('space'):
        paused = not paused
        if paused:
            print("\nProgram PAUSED. Press Space to resume.")
        else:
            print("\nProgram RESUMED.")
        time.sleep(0.3)

    if keyboard.is_pressed('r'):
        start_time = time.time()
        elapsed_time = 0
        print("\nTimer reset!")
        time.sleep(0.3)

    if paused:
        time.sleep(0.1)
        continue

    speed_category = get_speed_category(elapsed_time)
    
    if keyboard.is_pressed('left') or keyboard.is_pressed('a'):
        if selection_area:
            snapshot = ImageGrab.grab(bbox=selection_area)
        else:
            snapshot = ImageGrab.grab()
        save_path = os.path.join(base_screens_path, speed_category, "LEFT", 
                                f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{datetime.datetime.now().microsecond//1000:03d}.png")
        snapshot.save(save_path)
        print(f"\nScreenshot saved to {save_path}")
        time.sleep(0.1)
    
    elif keyboard.is_pressed('right') or keyboard.is_pressed('d'):
        if selection_area:
            snapshot = ImageGrab.grab(bbox=selection_area)
        else:
            snapshot = ImageGrab.grab()
        save_path = os.path.join(base_screens_path, speed_category, "RIGHT", 
                                f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{datetime.datetime.now().microsecond//1000:03d}.png")
        snapshot.save(save_path)
        print(f"\nScreenshot saved to {save_path}")
        time.sleep(0.1)
        
    elif keyboard.is_pressed('up') or keyboard.is_pressed('w'):
        if selection_area:
            snapshot = ImageGrab.grab(bbox=selection_area)
        else:
            snapshot = ImageGrab.grab()
        save_path = os.path.join(base_screens_path, speed_category, "UP", 
                                f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{datetime.datetime.now().microsecond//1000:03d}.png")
        snapshot.save(save_path)
        print(f"\nScreenshot saved to {save_path}")
        time.sleep(0.1)
          
    elif keyboard.is_pressed('down') or keyboard.is_pressed('s'):
        if selection_area:
            snapshot = ImageGrab.grab(bbox=selection_area)
        else:
            snapshot = ImageGrab.grab()
        save_path = os.path.join(base_screens_path, speed_category, "DOWN", 
                                f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{datetime.datetime.now().microsecond//1000:03d}.png")
        snapshot.save(save_path)
        print(f"\nScreenshot saved to {save_path}")
        time.sleep(0.1)
    
    elif keyboard.is_pressed('ctrl'):
        if selection_area:
            snapshot = ImageGrab.grab(bbox=selection_area)
        else:
            snapshot = ImageGrab.grab()
        save_path = os.path.join(base_screens_path, speed_category, "NONE", 
                                f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{datetime.datetime.now().microsecond//1000:03d}.png")
        snapshot.save(save_path)
        print(f"\nScreenshot saved to {save_path}")
        time.sleep(0.1)

    elif keyboard.is_pressed('esc') and keyboard.is_pressed('shift'):
        print("\nProgram terminated.")
        break
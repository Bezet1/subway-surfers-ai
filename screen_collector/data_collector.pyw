import os
from PIL import ImageGrab, Image
import keyboard
import time
import datetime
import tkinter as tk
from tkinter import messagebox
import pyautogui  
from src.screen_selector import select_screen_area

screens_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screens')
paused = False
selection_area = None

# Create folders for different directions
folder_names = ["LEFT", "RIGHT", "UP", "DOWN"]
for folder_name in folder_names:
    folder_path = os.path.join(screens_path, folder_name)
    try:
        os.mkdir(folder_path)
        print(f"Directory '{folder_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{folder_name}' already exists.")

# Ask user to select screen area
print("Please select the area of the screen you want to capture.")
selection_area = select_screen_area()

if selection_area:
    print(f"Selected area: {selection_area}")
    print("Program started. Press arrow keys or WASD to take screenshots.")
    print("Press Space to pause/resume. Press Shift+Esc to exit.")
else:
    print("No area selected. Using full screen capture.")

# Main loop
while True:
    if keyboard.is_pressed('space'):
        paused = not paused
        if paused:
            print("Program PAUSED. Press Space to resume.")
        else:
            print("Program RESUMED.")
        time.sleep(0.3)

    if paused:
        time.sleep(0.1)
        continue

    if keyboard.is_pressed('left') or keyboard.is_pressed('a'):
        if selection_area:
            snapshot = ImageGrab.grab(bbox=selection_area)
        else:
            snapshot = ImageGrab.grab()
        save_path = os.path.join(screens_path, "LEFT", f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{datetime.datetime.now().microsecond//1000:03d}.png")
        snapshot.save(save_path)
        print(f"Screenshot saved to {save_path}")
        time.sleep(0.1)
    
    elif keyboard.is_pressed('right') or keyboard.is_pressed('d'):
        if selection_area:
            snapshot = ImageGrab.grab(bbox=selection_area)
        else:
            snapshot = ImageGrab.grab()
        save_path = os.path.join(screens_path, "RIGHT", f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{datetime.datetime.now().microsecond//1000:03d}.png")
        snapshot.save(save_path)
        print(f"Screenshot saved to {save_path}")
        time.sleep(0.1)
        
    elif keyboard.is_pressed('up') or keyboard.is_pressed('w'):
        if selection_area:
            snapshot = ImageGrab.grab(bbox=selection_area)
        else:
            snapshot = ImageGrab.grab()
        save_path = os.path.join(screens_path, "UP", f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{datetime.datetime.now().microsecond//1000:03d}.png")
        snapshot.save(save_path)
        print(f"Screenshot saved to {save_path}")
        time.sleep(0.1)
          
    elif keyboard.is_pressed('down') or keyboard.is_pressed('s'):
        if selection_area:
            snapshot = ImageGrab.grab(bbox=selection_area)
        else:
            snapshot = ImageGrab.grab()
        save_path = os.path.join(screens_path, "DOWN", f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{datetime.datetime.now().microsecond//1000:03d}.png")
        snapshot.save(save_path)
        print(f"Screenshot saved to {save_path}")
        time.sleep(0.1)

    elif keyboard.is_pressed('esc') and keyboard.is_pressed('shift'):
        print("Program terminated.")
        break
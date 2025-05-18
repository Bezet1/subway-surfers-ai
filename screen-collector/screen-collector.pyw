import os
from PIL import ImageGrab, Image
import keyboard
import time
import datetime
import tkinter as tk
from tkinter import messagebox
import pyautogui  

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

# Function to select screen area
def select_screen_area():
    global selection_area
    
    # Get the actual screen resolution
    screen_width, screen_height = pyautogui.size()
    print(f"Detected screen resolution: {screen_width}x{screen_height}")
    
    # Create a full-screen window
    root = tk.Tk()
    root.title("Select capture area")
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    root.configure(bg='grey')
    
    # Variables to store selection coordinates
    start_x, start_y = 0, 0
    end_x, end_y = 0, 0
    rectangle_id = None
    
    # Canvas adjusted to screen size
    canvas = tk.Canvas(root, bg='grey', highlightthickness=0, width=screen_width, height=screen_height)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Function handling mouse button press
    def on_press(event):
        nonlocal start_x, start_y, rectangle_id
        start_x, start_y = event.x, event.y
        if rectangle_id:
            canvas.delete(rectangle_id)
        rectangle_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, 
                                             outline='red', width=2)
    
    # Function handling mouse movement
    def on_move(event):
        nonlocal end_x, end_y, rectangle_id
        end_x, end_y = event.x, event.y
        if rectangle_id:
            canvas.coords(rectangle_id, start_x, start_y, end_x, end_y)
            
            # Display selection dimensions
            width = abs(end_x - start_x)
            height = abs(end_y - start_y)
            canvas.delete("info_text")
            canvas.create_text((start_x + end_x) // 2, min(start_y, end_y) - 10,
                             text=f"Dimensions: {width}x{height} px", fill="white", 
                             tags="info_text")
    
    # Function handling mouse button release
    def on_release(event):
        nonlocal start_x, start_y, end_x, end_y
        end_x, end_y = event.x, event.y
        
        # Ensure coordinates are in correct order (top-left to bottom-right)
        if start_x > end_x:
            start_x, end_x = end_x, start_x
        if start_y > end_y:
            start_y, end_y = end_y, start_y
        
        # Check if selection is not too small
        if abs(end_x - start_x) < 10 or abs(end_y - start_y) < 10:
            canvas.delete(rectangle_id)
            canvas.create_text(screen_width//2, screen_height//2, 
                             text="Selection too small. Please try again.", 
                             fill="white", font=("Arial", 14))
            return
        
        # Save selection area and close window
        global selection_area
        selection_area = (start_x, start_y, end_x, end_y)
        root.destroy()
    
    # Bind mouse events
    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_move)
    canvas.bind("<ButtonRelease-1>", on_release)
    
    
    # Cancel button
    cancel_button = tk.Button(root, text="Cancel", command=root.destroy)
    cancel_button.place(relx=0.5, rely=0.95, anchor='center')
    
    root.mainloop()
    
    return selection_area

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
import os
from PIL import ImageGrab, Image
import keyboard
import time
import datetime
import tkinter as tk
from tkinter import messagebox
import pyautogui  

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
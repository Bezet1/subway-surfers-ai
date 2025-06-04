from src.config import DATA_DIR, MODEL_PATH, CLASS_NAMES, SAMPLE_IMAGE_PATH
import tensorflow as tf
import os
from screen_collector.src.screen_selector import select_screen_area
import keyboard
import time
from PIL import ImageGrab
from utils.predict import predict_image
import numpy as np

# Parametry
DELAY = 0.5  # Opóźnienie między odczytami (w sekundach)
precision_threshold = 0.85  # Obniżamy próg pewności
paused = False  # Flaga pauzy

# Sprawdzanie, czy model istnieje
if not os.path.exists(MODEL_PATH):
  print("\nModel not found. Quit...")
  exit()

print("\nModel found. Loading existing model...")
model = tf.keras.models.load_model(MODEL_PATH)

# Wypisanie informacji o modelu dla diagnostyki
print("\nInformacje o modelu:")
print(f"Oczekiwane klasy: {CLASS_NAMES}")

# Statystyki dla każdej klasy
class_stats = {class_name: {'count': 0, 'correct': 0} for class_name in CLASS_NAMES}

# Wybór obszaru ekranu
selection_area = select_screen_area()

if not selection_area:
  print("No screen area selected. Quit...")
  exit()

# Funkcja do wykonania ruchu z dodatkową diagnostyką
def execute_move(predicted_class, confidence):
  print(f"\nWykonanie ruchu: {predicted_class}, pewność: {confidence:.4f}")
  
  # Aktualizacja statystyk
  class_stats[predicted_class]['count'] += 1
  
  # Wykonanie akcji odpowiadającej przewidywanej klasie
  if predicted_class == "LEFT":
    print("\nWykonuję ruch w LEWO")
    keyboard.press_and_release('left')
  elif predicted_class == "RIGHT":
    print("\nWykonuję ruch w PRAWO")
    keyboard.press_and_release('right')
  elif predicted_class == "UP":
    print("\nWykonuję ruch w GÓRĘ")
    keyboard.press_and_release('up')
  elif predicted_class == "DOWN":
    print("\nWykonuję ruch w DÓŁ")
    keyboard.press_and_release('down')
  elif predicted_class == "NONE":
    print("\nNONE - Brak akcji")
  else:
    print(f"\nNieznana klasa: {predicted_class}")

# Główna pętla programu
print("\nProgram started. Press Space to pause/resume, Esc to quit.")
print(f"Using class names: {CLASS_NAMES}")

# Licznik klatek
frame_count = 0

while True:
  # Obsługa pauzy
  if keyboard.is_pressed('space'):
    paused = not paused
    print("Program PAUSED. Press Space to resume." if paused else "Program RESUMED.")
    time.sleep(0.3)  # Opóźnienie aby uniknąć wielokrotnego przełączania
  
  # Obsługa wyjścia
  if keyboard.is_pressed('esc'):
    print("\nProgram terminated.")
    
    # Wyświetl statystyki
    print("\nStatystyki przewidywań:")
    for class_name, stats in class_stats.items():
      print(f"{class_name}: {stats['count']} przewidywań")
    
    break

  if paused:
    time.sleep(0.1)
    continue

  try:
    # Zrobienie zrzutu ekranu
    snapshot = ImageGrab.grab(bbox=selection_area)
    frame_count += 1
    
    # Przewidywanie klasy
    predicted_class, confidence = predict_image(model, snapshot, class_names=CLASS_NAMES)
    
    # Wyświetlenie wyników
    print(f"\n[Klatka {frame_count}] Przewidywana klasa: {predicted_class}, pewność: {confidence:.4f}")
    
    # Wykonanie ruchu, jeśli pewność jest wystarczająca
    if confidence >= precision_threshold:
      execute_move(predicted_class, confidence)
    else:
      print(f"Pewność {confidence:.4f} poniżej progu {precision_threshold} - brak akcji")
  
  except Exception as e:
    print(f"Błąd podczas przewidywania: {e}")
  
  # Opóźnienie przed następnym odczytem
  time.sleep(DELAY)
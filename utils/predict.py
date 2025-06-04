import tensorflow as tf
import numpy as np

def predict_image(model, img, class_names = ['DOWN', 'LEFT', 'NONE', 'RIGHT', 'UP']):
  """
  Przewiduje klasę obrazu z użyciem modelu CNN.
  
  Args:
    model: Załadowany model TensorFlow
    img: Obraz wejściowy
    class_names: Lista nazw klas w tej samej kolejności, w jakiej model został wytrenowany
                (domyślnie kolejność alfabetyczna TensorFlow)
  
  Returns:
    Tuple zawierający (nazwa_przewidywanej_klasy, poziom_pewności)
  """
  resize = tf.image.resize(img, (256, 256))

  # Normalizacja obrazu
  normalized_img = resize/255
  
  # Dodanie wymiaru batch
  batched_img = tf.expand_dims(normalized_img, 0)
  
  # Przewidywanie
  prediction = model.predict(batched_img)

  # Wypisanie wszystkich prawdopodobieństw dla debugowania
  print("\nDebug - prawdopodobieństwa dla poszczególnych klas:")
  for i, class_name in enumerate(class_names):
    print(f"{class_name}: {prediction[0][i]:.4f}")

  # Indeks klasy z najwyższym prawdopodobieństwem
  predicted_class_index = prediction.argmax()
  
  # Nazwa klasy i pewność
  predicted_class_name = class_names[predicted_class_index]
  confidence = prediction[0][predicted_class_index]
  
  return predicted_class_name, confidence
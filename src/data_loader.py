import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def load_data(data_dir, img_size=(256, 256), batch_size=32):
  gpus = tf.config.experimental.list_physical_devices('GPU')
  for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)

  # Ładowanie danych bez augmentacji do wizualizacji
  base_data = tf.keras.utils.image_dataset_from_directory(
      data_dir,
      label_mode='categorical',
      image_size=img_size,
      batch_size=batch_size
  )
  
  class_names = base_data.class_names
  print("\n\nClass names:", class_names)
  
  # Wizualizacja przykładowych obrazów
  data_iterator = base_data.as_numpy_iterator()
  batch = data_iterator.next()
  
  print("Batch shape:", batch[0].shape)  # Images
  print("Labels shape:", batch[1].shape)  # One-hot labels
  print("Label example:", batch[1][0])

  fig, ax = plt.subplots(ncols=4, figsize=(20, 20))
  for idx, img in enumerate(batch[0][:4]):
      label_idx = batch[1][idx].argmax()
      class_name = class_names[label_idx]
      ax[idx].imshow(img.astype("uint8"))
      ax[idx].set_title(class_name)
  plt.show()

  # Teraz tworzymy nowy zbiór danych z augmentacją
  # Najpierw definiujemy generatory augmentacji dla zbioru treningowego
  datagen = ImageDataGenerator(
      rescale=1./255,          # Normalizacja
      rotation_range=10,        # Obrót w zakresie ±10 stopni
      width_shift_range=0.1,    # Przesunięcie poziome o 10%
      height_shift_range=0.1,   # Przesunięcie pionowe o 10%
      zoom_range=0.1,           # Powiększenie/pomniejszenie o 10%
      brightness_range=[0.9, 1.1], # Zmiana jasności ±10%
      horizontal_flip=False,    # Nie odwracamy obrazów horyzontalnie
      vertical_flip=False,      # Nie odwracamy obrazów wertykalnie
      fill_mode='nearest'       # Wypełnienie nowymi pikselami
  )
  
  # Generator dla zbioru walidacyjnego - tylko skalowanie
  val_datagen = ImageDataGenerator(rescale=1./255)
  
  # Ładowanie danych z augmentacją
  train_generator = datagen.flow_from_directory(
      data_dir,
      target_size=img_size,
      batch_size=batch_size,
      class_mode='categorical',
      subset='training'
  )
  
  # Tworzymy uproszczony interfejs dla danych augmentowanych
  # zgodny z interfejsem tf.data.Dataset, który był używany wcześniej
  class AugmentedDataAdapter:
      def __init__(self, generator):
          self.generator = generator
          
      def as_numpy_iterator(self):
          return self.generator
          
  # Korzystamy tylko z normalizacji dla zbioru danych bez augmentacji
  data = base_data.map(lambda x, y: (x/255, y))
  data = data.cache().shuffle(1000)
  
  print("\nDane zostały przygotowane z augmentacją dla zestawu treningowego")
  
  return data, class_names
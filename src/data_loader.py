import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

def load_data(data_dir, img_size=(224, 224), batch_size=16, validation_split=0.2, test_split=0.1):
  gpus = tf.config.experimental.list_physical_devices('GPU')
  for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)

  full_data = tf.keras.utils.image_dataset_from_directory(
      data_dir,
      label_mode='categorical',
      image_size=img_size,
      batch_size=batch_size,
      shuffle=True,
      seed=42
  )

  class_names = full_data.class_names
  
  total_batches = tf.data.experimental.cardinality(full_data).numpy()
  test_size = int(total_batches * test_split)
  val_size = int(total_batches * validation_split)
  train_size = total_batches - val_size - test_size
  
  train_data = full_data.take(train_size)
  remaining_data = full_data.skip(train_size)
  val_data = remaining_data.take(val_size)
  test_data = remaining_data.skip(val_size)
  
  def safe_augment(image, label):
      image = tf.image.random_brightness(image, max_delta=0.1)
      image = tf.image.random_contrast(image, lower=0.9, upper=1.1)
      
      return image, label

  def preprocess(image, label):
      image = tf.cast(image, tf.float32) / 255.0
      return image, label

  train_data = train_data.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
  val_data = val_data.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
  
  train_data = train_data.map(safe_augment, num_parallel_calls=tf.data.AUTOTUNE)
  
  train_data = train_data.cache().shuffle(1000).prefetch(tf.data.AUTOTUNE)
  val_data = val_data.cache().prefetch(tf.data.AUTOTUNE)
  
  sample_batch = next(iter(train_data.take(1)))
  images, labels = sample_batch
  
  print(f"Class names: {class_names}")
  print(f"Batch shape: {images.shape}")
  print(f"Labels shape: {labels.shape}")
  
  label_indices = tf.argmax(labels, axis=1).numpy()
  unique, counts = np.unique(label_indices, return_counts=True)
  
  print("Classes in batch:")
  for idx, count in zip(unique, counts):
      print(f"  {class_names[idx]}: {count}")
  
  fig, axes = plt.subplots(2, 4, figsize=(16, 8))
  axes = axes.flatten()
  
  for i in range(min(8, len(images))):
      label_idx = tf.argmax(labels[i]).numpy()
      class_name = class_names[label_idx]
      
      axes[i].imshow(images[i])
      axes[i].set_title(f"{class_name}")
      axes[i].axis('off')
  
  plt.tight_layout()
  plt.show()
  
  return train_data, val_data, test_data, class_names
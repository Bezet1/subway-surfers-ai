import matplotlib.pyplot as plt
import tensorflow as tf

def load_data(data_dir, img_size=(256, 256), batch_size=32):
  gpus = tf.config.experimental.list_physical_devices('GPU')
  for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)

  data = tf.keras.utils.image_dataset_from_directory(
      data_dir,
      label_mode='categorical',       # one-hot labels
      image_size=img_size,          # resize all images
      batch_size=batch_size
  )

  data_iterator = data.as_numpy_iterator()
  batch = data_iterator.next()
  class_names = data.class_names

  print("\n\nClass names:", class_names)
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

  data = data.map(lambda x, y: (x/255, y))
  data = data.cache().shuffle(1000)

  return data, class_names
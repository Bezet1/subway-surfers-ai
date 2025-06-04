from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np

def plot_confusion_matrix(model, val_data, class_names):
  y_pred = []
  y_true = []

  for x_batch, y_batch in val_data:
    preds = model.predict(x_batch)
    y_pred.extend(np.argmax(preds, axis=1))
    y_true.extend(np.argmax(y_batch, axis=1))

  cm = confusion_matrix(y_true, y_pred)
  disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
  disp.plot(xticks_rotation=45)
  plt.title("Confusion Matrix")
  plt.show()

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

    # Podstawowe sprawdzenia
    if len(y_true) == 0:
        print("Warning: No validation data, skipping confusion matrix")
        return
    
    if len(np.unique(y_true)) < 2:
        print("Warning: Only one class in validation data, skipping confusion matrix")
        return

    # Sprawdź które klasy rzeczywiście występują w danych
    unique_classes = np.unique(np.concatenate([y_true, y_pred]))
    actual_class_names = [class_names[i] for i in unique_classes]

    cm = confusion_matrix(y_true, y_pred, labels=unique_classes)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=actual_class_names)
    disp.plot(xticks_rotation=45)
    plt.title("Confusion Matrix")
    plt.show()
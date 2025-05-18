from tensorflow.keras.metrics import Precision, Recall, CategoricalAccuracy

def evaluate_model(model, test_data):
  pre = Precision()
  rec = Recall()
  acc = CategoricalAccuracy()
  
  for x, y in test_data.as_numpy_iterator():
    y_pred = model.predict(x)
    pre.update_state(y, y_pred)
    rec.update_state(y, y_pred)
    acc.update_state(y, y_pred)
  
  return {
    "precision": pre.result().numpy(),
    "recall": rec.result().numpy(),
    "accuracy": acc.result().numpy()
  }

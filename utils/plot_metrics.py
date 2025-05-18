import matplotlib.pyplot as plt

def plot_training_metrics(hist):
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))

    # Plot Loss
    ax1.plot(hist.history['loss'], color='blue', label='loss')
    ax1.plot(hist.history['val_loss'], color='orange', label='val_loss')
    ax1.set_title('Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend(loc='upper right')

    # Plot Accuracy
    ax2.plot(hist.history['accuracy'], color='green', label='accuracy')
    ax2.plot(hist.history['val_accuracy'], color='red', label='val_accuracy')
    ax2.set_title('Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend(loc='lower right')

    fig.suptitle('Training Metrics', fontsize=16)
    plt.tight_layout()
    plt.show()

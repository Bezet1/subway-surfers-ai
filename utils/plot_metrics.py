import matplotlib.pyplot as plt
import numpy as np

def plot_training_metrics(hist):
    # Utworzenie 2x2 wykresu dla lepszej analizy
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

    # 1. Wykres strat (Loss)
    ax1.plot(hist.history['loss'], color='blue', label='loss')
    ax1.plot(hist.history['val_loss'], color='orange', label='val_loss')
    ax1.set_title('Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend(loc='upper right')
    
    # Dodanie zacieniowanego obszaru pokazującego różnicę między treningiem a walidacją
    epochs = range(1, len(hist.history['loss']) + 1)
    ax1.fill_between(epochs, hist.history['loss'], hist.history['val_loss'], 
                   alpha=0.2, color='red' if np.mean(np.array(hist.history['val_loss']) > np.array(hist.history['loss'])) else 'green')
    
    # 2. Wykres dokładności (Accuracy)
    ax2.plot(hist.history['accuracy'], color='green', label='accuracy')
    ax2.plot(hist.history['val_accuracy'], color='red', label='val_accuracy')
    ax2.set_title('Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend(loc='lower right')
    ax2.fill_between(epochs, hist.history['accuracy'], hist.history['val_accuracy'], 
                   alpha=0.2, color='red' if np.mean(np.array(hist.history['accuracy']) > np.array(hist.history['val_accuracy'])) else 'green')

    # 3. Wykres różnicy między treningiem a walidacją (miara overfittingu)
    train_val_loss_diff = np.array(hist.history['loss']) - np.array(hist.history['val_loss'])
    ax3.plot(train_val_loss_diff, color='purple', label='train-val loss diff')
    ax3.axhline(y=0, color='r', linestyle='-', alpha=0.3)
    ax3.set_title('Train-Validation Loss Difference\n(Positive values suggest underfitting, negative suggest overfitting)')
    ax3.set_xlabel('Epoch')
    ax3.set_ylabel('Difference')
    ax3.legend(loc='lower right')
    
    # 4. Wykres learning rate, jeśli dostępny
    if 'lr' in hist.history:
        ax4.plot(hist.history['lr'], color='brown', label='Learning Rate')
        ax4.set_title('Learning Rate')
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Learning Rate')
        ax4.set_yscale('log')  # Skala logarytmiczna dla lepszej wizualizacji
        ax4.legend(loc='upper right')
    else:
        # Wykres zbliżenia na ostatnie epoki straty
        last_epochs = min(10, len(hist.history['loss']))
        ax4.plot(range(len(hist.history['loss'])-last_epochs, len(hist.history['loss'])), 
                hist.history['loss'][-last_epochs:], color='blue', label='loss (last epochs)')
        ax4.plot(range(len(hist.history['val_loss'])-last_epochs, len(hist.history['val_loss'])), 
                hist.history['val_loss'][-last_epochs:], color='orange', label='val_loss (last epochs)')
        ax4.set_title(f'Loss (Last {last_epochs} Epochs)')
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Loss')
        ax4.legend(loc='upper right')

    # Detekcja overfittingu
    overfit_analysis = ""
    if len(hist.history['loss']) > 5:
        # Sprawdzenie, czy val_loss zaczyna rosnąć, podczas gdy loss nadal spada
        early_val_loss = np.mean(hist.history['val_loss'][:3])
        late_val_loss = np.mean(hist.history['val_loss'][-3:])
        early_loss = np.mean(hist.history['loss'][:3])
        late_loss = np.mean(hist.history['loss'][-3:])
        
        if late_val_loss > early_val_loss and late_loss < early_loss:
            overfit_analysis = "Model wykazuje oznaki overfittingu: walidacyjna strata rośnie, podczas gdy treningowa spada."
        elif late_val_loss < early_val_loss and late_loss < early_loss:
            if (late_loss / early_loss) < 0.7 * (late_val_loss / early_val_loss):
                overfit_analysis = "Model może mieć lekki overfitting: treningowa strata spada szybciej niż walidacyjna."
            else:
                overfit_analysis = "Model uczy się dobrze bez wyraźnych oznak overfittingu."
    
    fig.suptitle(f'Training Metrics\n{overfit_analysis}', fontsize=16)
    plt.tight_layout()
    plt.show()
    
    # Wypisz analizę
    print("\nAnaliza procesu uczenia:")
    print(overfit_analysis)
    
    # Dodatkowe wskaźniki
    if len(hist.history['loss']) > 1:
        train_improvement = hist.history['loss'][0] - hist.history['loss'][-1]
        val_improvement = hist.history['val_loss'][0] - hist.history['val_loss'][-1]
        ratio = train_improvement / val_improvement if val_improvement > 0 else float('inf')
        
        print(f"Poprawa straty treningowej: {train_improvement:.4f}")
        print(f"Poprawa straty walidacyjnej: {val_improvement:.4f}")
        print(f"Stosunek poprawy (train/val): {ratio:.2f}")
        
        if ratio > 2:
            print("Sugestia: Model może cierpieć na overfitting. Rozważ silniejszą regularyzację.")
        elif ratio < 0.5:
            print("Sugestia: Model może być zbyt prosty. Rozważ zwiększenie jego pojemności.")
        else:
            print("Sugestia: Model ma dobrą równowagę między treningiem a walidacją.")
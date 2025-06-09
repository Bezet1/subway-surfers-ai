from src.config import *
from src.data_loader import load_data_improved
from src.model_builder import build_improved_cnn
from src.trainer import train_model_improved
from src.data_analyzer import analyze_dataset
from src.confusion_visualizer import plot_confusion_matrix
from src.evaluator import evaluate_model

def main():
    print("=== BOT SUBWAY SURFERS - TRENING ===")
    
    print("1. Analiza danych...")
    analyze_dataset(DATA_DIR, CLASS_NAMES)
    
    print("\n2. Ładowanie danych...")
    train_data, val_data, test_data, class_names = load_data_improved(
        DATA_DIR, 
        img_size=IMG_SIZE, 
        batch_size=BATCH_SIZE,
        validation_split=VALIDATION_SPLIT,
        test_split=TEST_SPLIT
    )
    
    print("\n3. Budowanie modelu...")
    model = build_improved_cnn(input_shape=(*IMG_SIZE, 3), num_classes=len(class_names))
    
    print(model.summary())
    
    print("\n4. Trening modelu...")
    history = train_model_improved(
        model, 
        train_data, 
        val_data, 
        MODEL_PATH,
        epochs=30,
        patience=10
    )
    
    print("✅ Trening zakończony!")
    
    plot_confusion_matrix(model, val_data, class_names)
    evaluate_model(model, test_data)
    
    return model, history

if __name__ == "__main__":
    main()

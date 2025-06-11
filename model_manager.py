from config import *
from src.data_loader import load_data
from src.model_builder import build_model
from src.trainer import train_model
from src.data_analyzer import analyze_dataset
from src.confusion_visualizer import plot_confusion_matrix
from src.evaluator import evaluate_model

def train_speed_model(speed_category, data_dir, model_path):
    print(f"=== BOT SUBWAY SURFERS - TRAINING {speed_category.upper()} MODEL ===")
    
    print(f"1. Analyzing {speed_category} data...")
    analyze_dataset(data_dir, CLASS_NAMES)
    
    print(f"\n2. Loading {speed_category} data...")
    train_data, val_data, test_data, class_names = load_data(
        data_dir, 
        img_size=IMG_SIZE, 
        batch_size=BATCH_SIZE,
        validation_split=VALIDATION_SPLIT,
        test_split=TEST_SPLIT
    )
    
    print(f"\n3. Building {speed_category} model...")
    model = build_model(input_shape=(*IMG_SIZE, 3), num_classes=len(class_names))
    
    print(model.summary())
    
    print(f"\n4. Training {speed_category} model...")
    history = train_model(
        model, 
        train_data, 
        val_data, 
        model_path,
        epochs=30,
        patience=10
    )
    
    print(f"{speed_category.upper()} model training completed!")
    
    plot_confusion_matrix(model, val_data, class_names)
    metrics = evaluate_model(model, test_data)
    
    print(f"{speed_category.upper()} model metrics:")
    for metric_name, metric_value in metrics.items():
        print(f"  {metric_name}: {metric_value:.4f}")
    
    return model, history

def main():
    # Create the models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Train slow model
    print("\n\n=== TRAINING SLOW MODEL ===")
    slow_model, slow_history = train_speed_model(SLOW_FOLDER, SLOW_DATA_DIR, SLOW_MODEL_PATH)
    
    # Train medium model
    print("\n\n=== TRAINING MEDIUM MODEL ===")
    medium_model, medium_history = train_speed_model(MEDIUM_FOLDER, MEDIUM_DATA_DIR, MEDIUM_MODEL_PATH)
    
    # Train fast model
    print("\n\n=== TRAINING FAST MODEL ===")
    fast_model, fast_history = train_speed_model(FAST_FOLDER, FAST_DATA_DIR, FAST_MODEL_PATH)
    
    print("\n=== ALL MODELS TRAINED SUCCESSFULLY ===")
    return {
        "slow": (slow_model, slow_history),
        "medium": (medium_model, medium_history),
        "fast": (fast_model, fast_history)
    }

if __name__ == "__main__":
    main()
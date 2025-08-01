import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import seaborn as sns

def analyze_dataset(data_dir, class_names):    
    print("=== DATASET ANALYSIS ===")
    
    class_stats = {}
    
    for class_name in class_names:
        class_path = os.path.join(data_dir, class_name)
        
        if not os.path.exists(class_path):
            print(f"ERROR: Folder {class_name} not found")
            continue
            
        image_files = [f for f in os.listdir(class_path) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        class_stats[class_name] = {
            'count': len(image_files),
            'files': image_files
        }
        
        sizes = []
        for i, img_file in enumerate(image_files[:10]):
            try:
                img_path = os.path.join(class_path, img_file)
                with Image.open(img_path) as img:
                    sizes.append(img.size)
            except Exception as e:
                print(f"Error processing {img_file}: {e}")
        
        class_stats[class_name]['sizes'] = sizes
    
    print("\n=== NUMBER OF IMAGES PER CLASS ===")
    counts = []
    labels = []
    
    for class_name, stats in class_stats.items():
        count = stats['count']
        print(f"{class_name}: {count} images")
        counts.append(count)
        labels.append(class_name)
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color=['red', 'blue', 'green', 'orange'])
    plt.title('Image Count Distribution per Class')
    plt.ylabel('Number of Images')
    for i, count in enumerate(counts):
        plt.text(i, count + max(counts)*0.01, str(count), ha='center')
    plt.show()
    
    min_count = min(counts)
    max_count = max(counts)
    imbalance_ratio = max_count / min_count if min_count > 0 else float('inf')
    
    print(f"\n=== BALANCE ANALYSIS ===")
    print(f"Minimum number of images: {min_count}")
    print(f"Maximum number of images: {max_count}")
    print(f"Imbalance ratio: {imbalance_ratio:.2f}")
    
    return class_stats
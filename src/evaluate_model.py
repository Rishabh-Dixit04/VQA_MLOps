import sys
import pandas as pd
import os
import random

# --- CONFIGURATION ---
DATA_ROOT = "data"
VQA_FILE = os.path.join(DATA_ROOT, "VQA_Dataset.csv")
META_FILE = os.path.join(DATA_ROOT, "abo-images-small/images/metadata/images.csv")

def evaluate():
    print("--- STARTING MODEL EVALUATION STAGE ---")
    
    # 1. Load Data
    try:
        vqa_df = pd.read_csv(VQA_FILE)
        meta_df = pd.read_csv(META_FILE)
        merged_df = pd.merge(vqa_df, meta_df, on='image_id', how='inner')
        
        # USE DIFFERENT SUBSET: Rows 50 to 70 (Unseen data)
        test_set = merged_df.iloc[50:70] 
        print(f"Loaded Test Set: {len(test_set)} items (Rows 50-70).")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # 2. Simulate Inference Loop
    # In a real scenario, you would load your model here:
    # model = AutoModel.from_pretrained("your_hub/vqa_model")
    
    correct_count = 0
    total_count = len(test_set)
    
    print("Running Batch Inference...")
    for index, row in test_set.iterrows():
        image_path = row['path'] # e.g., 14/14fe8812.jpg
        question = row['question']
        ground_truth = str(row['answer'])
        
        # --- REAL MODEL CALL WOULD GO HERE ---
        # predicted = model.predict(image_path, question)
        
        # For MLOps Demo: We simulate an 80% success rate
        # We randomly decide if the prediction was correct
        is_correct = random.random() < 0.8
        
        predicted = ground_truth if is_correct else "wrong_answer"
        
        if predicted == ground_truth:
            correct_count += 1
            
        # print(f"Q: {question} | Truth: {ground_truth} | Pred: {predicted}")

    # 3. Calculate Metrics
    accuracy = correct_count / total_count
    print(f"Evaluation Complete. Accuracy: {accuracy*100:.2f}%")
    
    # 4. The DevOps Gatekeeper Logic
    THRESHOLD = 0.70
    if accuracy < THRESHOLD:
        print("FAILED: Model accuracy is below acceptable threshold (70%). Deployment Aborted.")
        sys.exit(1) # Returns Error Code 1, Stopping Jenkins
    else:
        print("PASSED: Model quality verified. Proceeding to Docker Push.")
        sys.exit(0) # Returns Success Code 0

if __name__ == "__main__":
    evaluate()
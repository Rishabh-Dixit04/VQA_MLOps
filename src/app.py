# # # from flask import Flask, request, jsonify

# # # app = Flask(__name__)

# # # print("Initializing VQA Agent...")

# # # @app.route('/health', methods=['GET'])
# # # def health():
# # #     return jsonify({"status": "healthy"}), 200

# # # @app.route('/predict', methods=['POST'])
# # # def predict():
# # #     try:
# # #         data = request.json
# # #         # In a real app, you'd pass this to your model
# # #         question = data.get('question')
        
# # #         # Log for ELK Stack monitoring
# # #         print(f"LOG_EVENT: Question: {question}")
        
# # #         return jsonify({"answer": "Simulated Answer"}), 200
# # #     except Exception as e:
# # #         return jsonify({"error": str(e)}), 500

# # # if __name__ == "__main__":
# # #     # Host must be 0.0.0.0 to be accessible outside the container
# # #     app.run(host='0.0.0.0', port=5000)


# # # import os
# # # import torch
# # # from flask import Flask, request, jsonify
# # # from PIL import Image
# # # from transformers import BlipProcessor, BlipForQuestionAnswering
# # # from peft import PeftModel

# # # app = Flask(__name__)

# # # # --- CONFIGURATION ---
# # # # Path where Minikube mounts the 3GB dataset
# # # DATA_ROOT = "/app/data/abo-images-small/images/small"

# # # # 1. The Base Model (Heavy, Pre-trained)
# # # BASE_MODEL_ID = "Salesforce/blip-vqa-capfilt-large"

# # # # 2. Your Fine-Tuned Adapter (from HuggingFace)
# # # ADAPTER_ID = "RishabhD04/VQA_Fine-Tuned" 

# # # print(f"Initializing VQA Agent...")
# # # print(f"Base Model: {BASE_MODEL_ID}")
# # # print(f"Adapter: {ADAPTER_ID}")

# # # try:
# # #     # Use CPU to avoid Minikube driver issues (though slow, it is stable)
# # #     device = "cpu" 
    
# # #     # 1. Load Processor
# # #     processor = BlipProcessor.from_pretrained(BASE_MODEL_ID)
    
# # #     # 2. Load Base Model
# # #     print("Loading Base Model...")
# # #     base_model = BlipForQuestionAnswering.from_pretrained(BASE_MODEL_ID)
    
# # #     # 3. Load & Merge Your Adapter
# # #     print("Loading and Merging Adapter...")
# # #     model = PeftModel.from_pretrained(base_model, ADAPTER_ID)
# # #     model.eval().to(device)
    
# # #     print("VQA Model Loaded Successfully!")
# # # except Exception as e:
# # #     print(f"CRITICAL ERROR LOADING MODEL: {e}")
# # #     model = None

# # # @app.route('/health', methods=['GET'])
# # # def health():
# # #     if model:
# # #         return jsonify({"status": "healthy", "model": "loaded"}), 200
# # #     return jsonify({"status": "unhealthy", "reason": "model_failed"}), 500

# # # @app.route('/predict', methods=['POST'])
# # # def predict():
# # #     if not model:
# # #         return jsonify({"error": "Model not initialized"}), 500

# # #     try:
# # #         data = request.json
# # #         image_rel_path = data.get('image_path') 
# # #         question = data.get('question')
        
# # #         # Construct full path
# # #         image_path = os.path.join(DATA_ROOT, image_rel_path)
# # #         print(f"LOG_EVENT: Processing Q: '{question}' for Image: {image_path}")
        
# # #         if not os.path.exists(image_path):
# # #              return jsonify({"error": f"Image not found at {image_path}"}), 404
             
# # #         # 1. Load Image
# # #         raw_image = Image.open(image_path).convert('RGB')

# # #         # 2. Run Inference
# # #         inputs = processor(raw_image, question, return_tensors="pt").to(device)
        
# # #         with torch.no_grad():
# # #             out = model.generate(**inputs)
            
# # #         answer = processor.decode(out[0], skip_special_tokens=True)
        
# # #         print(f"LOG_EVENT: Answer Generated: {answer}")
        
# # #         return jsonify({"question": question, "answer": answer}), 200

# # #     except Exception as e:
# # #         print(f"ERROR: {e}")
# # #         return jsonify({"error": str(e)}), 500

# # # if __name__ == "__main__":
# # #     app.run(host='0.0.0.0', port=5000)

# # import os
# # import torch
# # from flask import Flask, request, jsonify
# # from PIL import Image
# # from transformers import BlipProcessor, BlipForQuestionAnswering
# # from peft import PeftModel

# # app = Flask(__name__)

# # # --- CONFIGURATION ---
# # # 1. BASE MODEL: Loaded from the mounted volume (Local)
# # # Since you mounted './data' to '/app/data', the model is here:
# # BASE_MODEL_PATH = "/app/data/blip-large"

# # # 2. ADAPTER: Fetched from HuggingFace (Cloud)
# # ADAPTER_ID = "RishabhD04/VQA_Fine-Tuned" 

# # # 3. DATASET: Mounted volume
# # DATA_ROOT = "/app/data/abo-images-small/images/small"

# # print(f"Initializing VQA Agent...")
# # print(f"Loading Base Model from Disk: {BASE_MODEL_PATH}")

# # try:
# #     device = "cpu"
    
# #     # Load Base from Disk (Fast & Stable)
# #     processor = BlipProcessor.from_pretrained(BASE_MODEL_PATH, local_files_only=True)
# #     base_model = BlipForQuestionAnswering.from_pretrained(BASE_MODEL_PATH, local_files_only=True)
    
# #     # Load Adapter from Cloud (Small file, so network won't timeout)
# #     print(f"Fetching Adapter from HF: {ADAPTER_ID}")
# #     model = PeftModel.from_pretrained(base_model, ADAPTER_ID)
# #     model.eval().to(device)
    
# #     print("VQA Model Ready!")
# # except Exception as e:
# #     print(f"CRITICAL ERROR: {e}")
# #     model = None

# # @app.route('/health', methods=['GET'])
# # def health():
# #     return jsonify({"status": "healthy"}), 200 if model else 500

# # @app.route('/predict', methods=['POST'])
# # def predict():
# #     if not model: return jsonify({"error": "Model not loaded"}), 500
# #     try:
# #         data = request.json
# #         image_path = os.path.join(DATA_ROOT, data.get('image_path'))
# #         question = data.get('question')
        
# #         if not os.path.exists(image_path): return jsonify({"error": "Image not found"}), 404
        
# #         raw_image = Image.open(image_path).convert('RGB')
# #         inputs = processor(raw_image, question, return_tensors="pt").to(device)
        
# #         with torch.no_grad():
# #             out = model.generate(**inputs)
# #         answer = processor.decode(out[0], skip_special_tokens=True)
        
# #         return jsonify({"answer": answer}), 200
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # if __name__ == "__main__":
# #     app.run(host='0.0.0.0', port=5000)

# import os
# import torch
# from flask import Flask, request, jsonify
# from PIL import Image
# from transformers import BlipProcessor, BlipForQuestionAnswering
# from peft import PeftModel

# app = Flask(__name__)

# # --- CONFIGURATION ---
# DATA_ROOT = "/app/data/abo-images-small/images/small"
# BASE_MODEL_PATH = "/app/data/blip-large"
# ADAPTER_PATH = "/app/data/vqa-adapter" # <--- UPDATED to local path

# print(f"Initializing VQA Agent...")

# try:
#     device = "cpu"
    
#     # Load Processor & Base (Offline)
#     processor = BlipProcessor.from_pretrained(BASE_MODEL_PATH, local_files_only=True)
#     base_model = BlipForQuestionAnswering.from_pretrained(BASE_MODEL_PATH, local_files_only=True)
    
#     # Load Adapter (Offline)
#     print(f"Loading Adapter from {ADAPTER_PATH}...")
#     model = PeftModel.from_pretrained(base_model, ADAPTER_PATH, local_files_only=True)
#     model.eval().to(device)
    
#     print("VQA Model Loaded Successfully!")
# except Exception as e:
#     print(f"CRITICAL ERROR LOADING MODEL: {e}")
#     model = None

# @app.route('/health', methods=['GET'])
# def health():
#     return jsonify({"status": "healthy", "model": "loaded"}), 200 if model else 500

# @app.route('/predict', methods=['POST'])
# def predict():
#     if not model: return jsonify({"error": "Model not loaded"}), 500

#     try:
#         data = request.json
#         image_path = os.path.join(DATA_ROOT, data.get('image_path'))
#         question = data.get('question')
        
#         if not os.path.exists(image_path): 
#             return jsonify({"error": f"Image not found at {image_path}"}), 404
             
#         raw_image = Image.open(image_path).convert('RGB')
#         inputs = processor(raw_image, question, return_tensors="pt").to(device)
        
#         with torch.no_grad():
#             out = model.generate(**inputs)
#         answer = processor.decode(out[0], skip_special_tokens=True)
        
#         print(f"LOG_EVENT: Answer Generated: {answer}")
#         return jsonify({"question": question, "answer": answer}), 200

#     except Exception as e:
#         print(f"ERROR: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)

import os
import time
import torch
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering
from peft import PeftModel

app = Flask(__name__)

# --- CONFIGURATION ---
DATA_ROOT = "/app/data/abo-images-small/images/small"
BASE_MODEL_PATH = "/app/data/blip-large"
ADAPTER_PATH = "/app/data/vqa-adapter"

print(f"Initializing VQA Agent...")
try:
    device = "cpu"
    processor = BlipProcessor.from_pretrained(BASE_MODEL_PATH, local_files_only=True)
    base_model = BlipForQuestionAnswering.from_pretrained(BASE_MODEL_PATH, local_files_only=True)
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH, local_files_only=True)
    model.eval().to(device)
    print("VQA Model Loaded Successfully!")
except Exception as e:
    print(f"CRITICAL ERROR LOADING MODEL: {e}")
    model = None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    if not model: return jsonify({"error": "Model not loaded"}), 500
    
    start_time = time.time() # Start Timer

    try:
        data = request.json
        image_rel_path = data.get('image_path') 
        question = data.get('question')
        image_path = os.path.join(DATA_ROOT, image_rel_path)
        
        if not os.path.exists(image_path): 
             return jsonify({"error": f"Image not found"}), 404
             
        raw_image = Image.open(image_path).convert('RGB')
        inputs = processor(raw_image, question, return_tensors="pt").to(device)
        
        # --- GENERATION WITH CONFIDENCE SCORE ---
        with torch.no_grad():
            # output_scores=True allows us to see the probabilities
            outputs = model.generate(
                **inputs, 
                return_dict_in_generate=True, 
                output_scores=True,
                max_new_tokens=20
            )
        
        # Decode the Answer
        answer = processor.decode(outputs.sequences[0], skip_special_tokens=True)
        
        # Calculate Confidence (Quality Score)
        # We take the probabilities of the generated tokens
        confidence_score = 0.0
        if outputs.scores:
            # Stack scores from all generation steps
            scores = torch.stack(outputs.scores, dim=1)
            # Apply softmax to get probabilities
            probs = torch.nn.functional.softmax(scores, dim=-1)
            # Get the probability of the actual chosen tokens
            token_ids = outputs.sequences[:, 1:] # Skip start token
            # Gather the probabilities of the selected tokens
            token_probs = torch.gather(probs, 2, token_ids.unsqueeze(-1)).squeeze(-1)
            # Average probability represents the model's overall confidence
            confidence_score = torch.mean(token_probs).item()

        # Calculate Latency
        latency = time.time() - start_time
        
        # --- STRUCTURED LOGGING FOR ELK ---
        # This JSON structure is easy for Kibana to parse
        log_payload = {
            "event": "inference",
            "question": question,
            "answer": answer,
            "quality_score": round(confidence_score, 4), # Metric 1
            "latency_seconds": round(latency, 4)         # Metric 2
        }
        
        # Print with a special prefix so Filebeat finds it easily
        print(f"LOG_METRIC: {log_payload}")
        
        return jsonify(log_payload), 200

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
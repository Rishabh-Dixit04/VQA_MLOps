import os
from peft import PeftModel
from transformers import BlipForQuestionAnswering

# --- Configuration ---
BASE_MODEL_ID = "Salesforce/blip-vqa-capfilt-large"
ADAPTER_ID = "RishabhD04/VQA_Fine-Tuned"

# Save location: Inside your 'data' folder so it gets mounted automatically
SAVE_PATH = "./data/vqa-adapter"

print(f"1. Loading Base Model: {BASE_MODEL_ID}...")
# We need the base model structure to initialize the adapter
base_model = BlipForQuestionAnswering.from_pretrained(BASE_MODEL_ID)

print(f"2. Fetching Adapter: {ADAPTER_ID}...")
# This downloads your specific weights from Hugging Face
model = PeftModel.from_pretrained(base_model, ADAPTER_ID)

print(f"3. Saving Adapter to {SAVE_PATH}...")
model.save_pretrained(SAVE_PATH)

print("Success! Adapter weights are now local.")

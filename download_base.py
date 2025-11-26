from transformers import BlipProcessor, BlipForQuestionAnswering

# Download to the 'data' folder which is already mounted
save_path = "./data/blip-large" 
model_id = "Salesforce/blip-vqa-capfilt-large"

print(f"Downloading {model_id} to {save_path}...")
BlipProcessor.from_pretrained(model_id).save_pretrained(save_path)
BlipForQuestionAnswering.from_pretrained(model_id).save_pretrained(save_path)
print("Download Complete!")

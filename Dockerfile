# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# 1. Install CPU-only PyTorch explicitly FIRST
# We do this directly here to ensure we get the small CPU version (~150MB)
# instead of the default GPU version (~2GB).
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 2. Copy requirements file
COPY requirements.txt .

# 3. Install the rest of the dependencies
# Important: Ensure 'torch' is NOT in your requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the entire project folder (src, data, etc.) into /app
COPY . .

# 5. Expose the port Flask runs on
EXPOSE 5000

# 6. Command to run the app
# This path must match the file you just created: src/app.py
CMD ["python", "src/app.py"]
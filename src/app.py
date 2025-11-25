from flask import Flask, request, jsonify

app = Flask(__name__)

print("Initializing VQA Agent...")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # In a real app, you'd pass this to your model
        question = data.get('question')
        
        # Log for ELK Stack monitoring
        print(f"LOG_EVENT: Question: {question}")
        
        return jsonify({"answer": "Simulated Answer"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Host must be 0.0.0.0 to be accessible outside the container
    app.run(host='0.0.0.0', port=5000)



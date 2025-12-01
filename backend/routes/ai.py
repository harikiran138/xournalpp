from flask import Blueprint, request, jsonify
import time
import random
import requests
import json

ai_bp = Blueprint('ai', __name__)

# Mock AI Responses for Demo
MOCK_RESPONSES = [
    "Based on the diagram, this appears to be a biological cell structure. The nucleus is clearly visible.",
    "To solve this equation, first isolate the variable x by subtracting 5 from both sides.",
    "I've generated a 3-question quiz based on your notes:\n1. What is the powerhouse of the cell?\n2. Define mitosis.\n3. Explain the function of ribosomes.",
    "The concept you are drawing resembles a neural network architecture with input and hidden layers.",
]

@ai_bp.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint to handle AI chat requests.
    Proxies to local Ollama instance if available.
    """
    data = request.json
    user_message = data.get('message', '')
    context = data.get('context', {}) # Board elements context
    
    # Construct prompt with context
    system_prompt = "You are an AI assistant for NovaBoard, an educational whiteboard software. "
    if context:
        system_prompt += f"The user is currently working on a board with these elements: {json.dumps(context)}. "
    
    system_prompt += "Help the user with their teaching or learning tasks. Be concise."

    # Try connecting to local Ollama
    try:
        ollama_url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2", # Or whatever model is pulled
            "prompt": f"{system_prompt}\n\nUser: {user_message}\nAssistant:",
            "stream": False
        }
        
        # Check if model exists, if not try 'llama2' or 'mistral' or 'tinyllama'
        # For now, we assume the user followed instructions to pull a model.
        # We can make this robust by checking /api/tags first.
        
        response = requests.post(ollama_url, json=payload, timeout=10)
        if response.status_code == 200:
            ai_text = response.json().get('response', '')
            return jsonify({
                "role": "ai",
                "text": ai_text,
                "timestamp": time.time(),
                "source": "local-ollama"
            })
    except Exception as e:
        print(f"Ollama connection failed: {e}")
        # Fallback to mock if Ollama is down

    # Simulate processing delay (Thinking...)
    time.sleep(1.5)

    # Mock Response
    ai_response = random.choice(MOCK_RESPONSES)
    
    if "quiz" in user_message.lower():
        ai_response = "Here is a quick quiz:\n1. What is the derivative of x^2?\n2. What is the integral of 1/x?\n3. Define a limit."

    return jsonify({
        "role": "ai",
        "text": ai_response,
        "timestamp": time.time(),
        "source": "mock"
    })

@ai_bp.route('/generate-image', methods=['POST'])
def generate_image():
    """
    Endpoint to generate images (e.g., DALL-E).
    """
    # Mock response
    return jsonify({
        "url": "https://via.placeholder.com/512",
        "prompt": request.json.get('prompt')
    })

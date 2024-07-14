import requests
import json
import base64


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def generate_response_with_image(prompt, image_path, model="llava"):
    ollama_url = "http://ollama:11434/api/generate"
    
    image_base64 = encode_image(image_path)
    data = {
        "model": model,
        "prompt": prompt,
        "images": [image_base64]
    }

    try:
        response = requests.post(ollama_url, json=data, stream=True)
        response.raise_for_status()
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line)
                if 'response' in decoded_line:
                    full_response += decoded_line['response']
        return full_response.strip()
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def generate_response(prompt, model="llava"):
    ollama_url = "http://ollama:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
    }
    
    try:
        response = requests.post(ollama_url, json=data, stream=True)
        response.raise_for_status()
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line)
                if 'response' in decoded_line:
                    full_response += decoded_line['response']
        return full_response.strip()
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def chat(messages, model="llava"):
    ollama_url = "http://ollama:11434/api/chat"
    
    data = {
        "model": model,
        "messages": messages
    }
    
    try:
        response = requests.post(ollama_url, json=data, stream=True)
        response.raise_for_status()
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line)
                if 'message' in decoded_line and 'content' in decoded_line['message']:
                    full_response += decoded_line['message']['content']
        return full_response.strip()
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def test_ollama_connection():
    try:
        response = requests.get("http://ollama:11434")
        response.raise_for_status()
        return "Successfully connected to Ollama"
    except requests.exceptions.RequestException as e:
        return f"Failed to connect to Ollama: {str(e)}"


def list_models():
    try:
        response = requests.get("http://ollama:11434/api/tags")
        response.raise_for_status()
        return response.json()['models']
    except requests.exceptions.RequestException as e:
        return f"Error listing models: {str(e)}"

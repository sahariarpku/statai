#!/usr/bin/env python3
import sys
import json
import requests
import os

def read_api_key():
    # Try to get API key from environment variable
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if api_key:
        return api_key
    
    # Try to read from config file
    config_path = os.path.expanduser('~/Documents/Stata/ado/personal/statai_config.txt')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            line = f.readline().strip()
            if line.startswith('DEEPSEEK_API_KEY='):
                return line.split('=', 1)[1]
    
    return None

def chat_with_deepseek(message):
    api_key = read_api_key()
    if not api_key:
        print(json.dumps({"error": "API key not found"}))
        return
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Extract and print just the assistant's message
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']['content']
            print(message)
        else:
            print(json.dumps({"error": "Invalid response format from API"}))
            
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No message provided"}))
        sys.exit(1)
    
    message = sys.argv[1]
    chat_with_deepseek(message) 
#!/usr/bin/env python3
import sys
import json
import requests
import os
import os.path
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

def create_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=5,  # increased number of retries
        backoff_factor=2,  # increased backoff time between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]  # explicitly allow POST method retries
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def analyze_with_deepseek(prompt, var_file):
    # Try to get API key from environment or config file
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    
    if not api_key:
        # Try to read from Stata config file
        try:
            # Common Stata personal directory locations
            possible_paths = [
                os.path.expanduser("~/Library/Application Support/Stata/ado/personal/statai_config.txt"),
                os.path.expanduser("~/Documents/Stata/ado/personal/statai_config.txt"),
                os.path.expanduser("~/.stata/statai_config.txt"),
                "./statai_config.txt"
            ]
            
            for config_path in possible_paths:
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        for line in content.split('\n'):
                            if line.startswith('DEEPSEEK_API_KEY='):
                                api_key = line.split('=', 1)[1].strip()
                                break
                    if api_key:
                        break
        except Exception as e:
            print(f"Error reading config: {e}")
    
    if not api_key:
        print("Error: API key not found. Please set it using 'statai setkey <your_api_key>'")
        return
    
    # Read variables from file with their types/formats
    try:
        with open(var_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print("Error: No variables found in dataset")
                return
            
            # Parse variable information
            variables = []
            for line in content.split('\n'):
                if line.strip():
                    variables.append(line.strip())
                    
    except Exception as e:
        print(f"Error reading variable file: {str(e)}")
        return
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Create different prompts based on whether specific analysis is requested
    if prompt and prompt.lower().strip() not in ['', 'analyze', 'general']:
        # Specific analysis requested
        full_prompt = f"""You are a Stata statistical analysis expert. I have a dataset with the following variables:

{chr(10).join(variables)}

User's specific analysis request: {prompt}

Please provide detailed Stata commands and explanations for this analysis. Include:
1. Appropriate statistical methods
2. Data preparation steps if needed
3. Clear commenting (using * or //) 
4. Interpretation guidance

Format your response with both commands and explanations."""
        
        system_content = "You are a Stata expert. Provide comprehensive analysis with clear explanations and well-commented code."
        
    else:
        # General analysis - suggest appropriate analyses
        full_prompt = f"""You are a Stata statistical analysis expert. I have a dataset with the following variables:

{chr(10).join(variables)}

Based on these variables, please suggest appropriate statistical analyses. Consider:
- Descriptive statistics for all variables
- Appropriate visualizations  
- Correlation analysis where relevant
- Basic inferential tests if applicable

Provide detailed Stata commands with explanations and comments."""
        
        system_content = "You are a Stata expert. Analyze the variable types and suggest comprehensive statistical analysis with explanations."
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    # Create a session with retry logic
    session = create_session_with_retries()
    
    try:
        # First attempt with shorter timeout
        try:
            response = session.post(url, headers=headers, json=payload, timeout=45)  # increased initial timeout
            response.raise_for_status()
        except requests.exceptions.Timeout:
            # If timeout occurs, try again with longer timeout
            print("Initial request timed out. Retrying with longer timeout...")
            time.sleep(2)  # Add a small delay before retry
            response = session.post(url, headers=headers, json=payload, timeout=90)  # increased retry timeout
            response.raise_for_status()
            
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            # Clean up markdown formatting if present
            content = content.replace('```stata', '').replace('```', '').strip()
            print(content)
        else:
            print("Error: Unexpected API response format")
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to DeepSeek API: {str(e)}")
        print("Please try again in a few moments. If the problem persists:")
        print("1. Check your internet connection")
        print("2. Verify that api.deepseek.com is accessible")
        print("3. Ensure your API key is valid")
        print("4. Try using a different network if possible")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 statai_analyze.py [<prompt_file>] <var_file>")
        sys.exit(1)
    
    if len(sys.argv) == 2:
        # Only variable file provided - general analysis
        prompt = ""
        var_file = sys.argv[1]
    else:
        # Prompt file and variable file provided
        prompt_file = sys.argv[1]
        var_file = sys.argv[2]
        
        # Read prompt from file with proper encoding
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
        except Exception as e:
            print(f"Error reading prompt file: {str(e)}")
            sys.exit(1)
    
    analyze_with_deepseek(prompt, var_file)
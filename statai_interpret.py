#!/usr/bin/env python3
import sys
import json
import requests
import os
import re
import warnings
import time
from urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Suppress SSL warnings
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

def create_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=5,  # number of retries
        backoff_factor=2,  # wait 2, 4, 8, 16, 32 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

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

def read_variables(vars_file):
    try:
        with open(vars_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error reading variables file: {str(e)}")
        return None

def parse_summary_stats(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Print debug information
        print("Debug: Content of summary file:")
        print(content)
        print("\nDebug: End of content\n")
            
        # Skip header lines
        lines = content.strip().split('\n')
        if len(lines) < 3:  # Need at least header, separator, and one data line
            print("Debug: Not enough lines in summary file")
            return None
            
        variables = []
        for line in lines[2:]:  # Skip header and separator lines
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                var_name = parts[0].strip()
                obs = parts[1].strip()
                mean = parts[2].strip()
                std_dev = parts[3].strip()
                min_val = parts[4].strip()
                max_val = parts[5].strip()
                
                variables.append({
                    'name': var_name,
                    'obs': obs,
                    'mean': mean,
                    'std_dev': std_dev,
                    'min': min_val,
                    'max': max_val
                })
        
        if not variables:
            print("Debug: No variables parsed from summary file")
            return None
            
        return variables
            
    except Exception as e:
        print(f"Error parsing summary statistics: {str(e)}")
        return None

def interpret_with_deepseek(variables, var_info):
    api_key = read_api_key()
    if not api_key:
        print("Error: API key not found. Please set it using 'statai setkey <your_api_key>'")
        return
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Format the variables for the prompt
    var_text = "\n".join([
        f"{v['name']}: n={v['obs']}, M={v['mean']}, SD={v['std_dev']}, Range=[{v['min']}, {v['max']}]"
        for v in variables
    ])
    
    prompt = f"""You are a statistical analysis expert. Please provide an APA-style interpretation of the following summary statistics:

Variable Information:
{var_info}

Summary Statistics:
{var_text}

Please provide:
1. A clear, concise interpretation of the descriptive statistics
2. Focus on the key patterns and relationships between variables
3. Use APA style formatting
4. Include any notable observations about the data distribution
5. Keep the interpretation professional and academic

Format your response in clear paragraphs with proper APA style."""

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a statistical analysis expert specializing in APA-style interpretation of data."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    # Create a session with retry logic
    session = create_session_with_retries()
    
    try:
        # First attempt with shorter timeout
        try:
            print("Attempting to connect to DeepSeek API...")
            response = session.post(url, headers=headers, json=data, timeout=45, verify=False)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            # If timeout occurs, try again with longer timeout
            print("Initial request timed out. Retrying with longer timeout...")
            time.sleep(2)  # Add a small delay before retry
            response = session.post(url, headers=headers, json=data, timeout=90, verify=False)
            response.raise_for_status()
            
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']['content']
            print("\n" + message + "\n")
        else:
            print("Error: Invalid response format from API")
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to DeepSeek API: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Check your internet connection")
        print("2. Verify that api.deepseek.com is accessible")
        print("3. Ensure your API key is valid")
        print("4. Try using a different network if possible")
        print("5. If the problem persists, try again in a few minutes")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 statai_interpret.py <summary_file> <vars_file>")
        sys.exit(1)
    
    summary_file = sys.argv[1]
    vars_file = sys.argv[2]
    
    variables = parse_summary_stats(summary_file)
    var_info = read_variables(vars_file)
    
    if variables and var_info:
        interpret_with_deepseek(variables, var_info)
    else:
        print("Error: Could not parse summary statistics or variables information")
        if not variables:
            print("Failed to parse summary statistics")
        if not var_info:
            print("Failed to read variables information") 
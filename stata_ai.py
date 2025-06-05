import sys
import json
import pandas as pd
import pyreadstat
from litellm import completion
import os

def process_stata_request(data_path, prompt):
    try:
        # Read the Stata data using pyreadstat
        df, meta = pyreadstat.read_dta(data_path)
        
        # Create a context with data summary
        data_summary = {
            "variables": list(df.columns),
            "observations": len(df),
            "variable_labels": meta.variable_labels,
            "sample_data": df.head().to_dict()
        }
        
        # Construct the prompt with data context
        full_prompt = f"""
        You are a Stata expert. Given the following data summary:
        {json.dumps(data_summary, indent=2)}
        
        User request: {prompt}
        
        Please provide a Stata command that would help achieve this request.
        Only provide the command, no explanations.
        """
        
        # Call DeepSeek through LiteLLM
        response = completion(
            model="deepseek/deepseek-coder-6.7b-instruct",  # Using DeepSeek's model
            messages=[{"role": "user", "content": full_prompt}],
            api_base="https://api.deepseek.com/v1",  # DeepSeek API endpoint
            api_key=os.getenv("DEEPSEEK_API_KEY")  # Get API key from environment variable
        )
        
        # Extract the command from the response
        stata_command = response.choices[0].message.content.strip()
        
        return {"status": "success", "command": stata_command}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"status": "error", "message": "Invalid arguments"}))
        sys.exit(1)
        
    data_path = sys.argv[1]
    prompt = sys.argv[2]
    
    result = process_stata_request(data_path, prompt)
    print(json.dumps(result)) 
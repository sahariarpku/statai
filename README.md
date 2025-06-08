# statai - DeepSeek API Integration for Stata

A Stata package that integrates with DeepSeek API for advanced data analysis and interpretation.

## Installation

### Method 1: Using net install (Recommended)

1. Open Stata and run:
```stata
net install statai, from(https://raw.githubusercontent.com/sahariarpku/statai/main)
```

2. Verify installation:
```stata
statai help
```

### Method 2: Manual Installation

1. Download the package:
   - Visit [https://github.com/sahariarpku/statai](https://github.com/sahariarpku/statai)
   - Click the green "Code" button and select "Download ZIP"
   - Extract the ZIP file

2. Install in Stata:
   - Open Stata
   - Navigate to the extracted directory
   - Run the installation script:
```stata
cd /path/to/extracted/statai
do install.do
```

3. Verify installation:
```stata
statai help
```

## Prerequisites

- Stata 16 or later
- Python 3.7 or later
- Required Python packages:
  - requests
  - pandas
  - numpy

## Usage

1. Set your DeepSeek API key:
```stata
statai setkey your-api-key-here
```

2. Basic commands:
```stata
statai analyze              // General analysis of all variables
statai analyze 'prompt'     // Specific analysis request
statai interpret            // Interpret last summary statistics in APA style
statai help                 // Show help message
```

## Examples

1. General analysis:
```stata
statai analyze
```

2. Specific analysis request:
```stata
statai analyze 'what kind of regression can I do here?'
```

3. Interpret summary statistics:
```stata
summarize popgrowth lexp gnppc
statai interpret
```

## Troubleshooting

1. If you get a "command not found" error:
   - Verify the installation path
   - Try reinstalling the package

2. If you get API connection errors:
   - Check your internet connection
   - Verify your API key is correct
   - Ensure you have the required Python packages installed

## Author

- **Md Sahariar Rahman**
- Peking University
- Email: sahariar@stu.pku.edu.cn

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
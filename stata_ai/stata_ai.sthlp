{smcl}
{* *! version 1.0.0 2024}
{title:stata_ai}

{phang}
{bf:stata_ai} - AI-powered Stata command suggestion using DeepSeek and LiteLLM

{marker syntax}{...}
{title:Syntax}

{p 8 17 2}
{cmd:stata_ai} {it:"your prompt here"}

{marker description}{...}
{title:Description}

{pstd}
{cmd:stata_ai} is a Stata plugin that uses AI to suggest appropriate Stata commands based on your natural language prompts. 
It analyzes your current dataset and uses DeepSeek's model through LiteLLM to generate relevant Stata commands.

{marker requirements}{...}
{title:Requirements}

{pstd}
- Python 3.7 or later
- Required Python packages:
  - pandas
  - pyreadstat
  - litellm
- DeepSeek API key

{marker setup}{...}
{title:Setup}

{pstd}
1. Install Python dependencies:
{cmd}
pip install pandas pyreadstat litellm
{text}

2. Set your DeepSeek API key:
{cmd}
export DEEPSEEK_API_KEY='your-api-key-here'
{text}

{marker examples}{...}
{title:Examples}

{pstd}
Show summary statistics:
{cmd}
. stata_ai "show me the summary statistics for all numeric variables"
{text}

{pstd}
Create a scatter plot:
{cmd}
. stata_ai "create a scatter plot of income vs education"
{text}

{marker notes}{...}
{title:Notes}

{pstd}
- The plugin requires an active dataset to be loaded in Stata
- Make sure your Python environment is properly configured
- The plugin includes variable labels in its analysis for better command suggestions

{marker author}{...}
{title:Author}

{pstd}
Your Name
email@example.com 
{smcl}
{* *! statai v1.0 - DeepSeek API integration for Stata}
{* *! Author: Your Name}
{* *! Date: 2024-03-20}

{title:Title}

{p2colset 5 20 22 2}{...}
{p2col :{cmd:statai} {hline 2}}DeepSeek API integration for Stata{p_end}
{p2colreset}{...}

{title:Syntax}

{p 8 17 2}
{cmd:statai} {cmd:setkey} {it:api_key}

{p 8 17 2}
{cmd:statai} {cmd:analyze}

{p 8 17 2}
{cmd:statai} {cmd:interpret}

{title:Description}

{pstd}
{cmd:statai} is a Stata plugin that integrates with the DeepSeek API to perform automated data analysis.
The plugin provides three main subcommands:

{phang}
{cmd:statai setkey} stores your DeepSeek API key for future use. The key is saved in your Stata personal directory
and will persist between Stata sessions.

{phang}
{cmd:statai analyze} performs an automated analysis of your current dataset using the DeepSeek API.
It sends a preview of your data (first 10 rows) to the API and displays the analysis results.

{phang}
{cmd:statai interpret} interprets the last summary statistics command results in APA style. This command
is particularly useful after running {cmd:summarize} or similar commands. It will provide a professional,
academic interpretation of the descriptive statistics.

{title:Options}

{pstd}
{cmd:statai setkey} requires your DeepSeek API key as an argument.

{pstd}
{cmd:statai analyze} has no options. It uses the currently loaded dataset.

{pstd}
{cmd:statai interpret} has no options. It uses the results from the last summary statistics command.

{title:Examples}

{phang}
Set your DeepSeek API key:
{cmd:. statai setkey your-api-key-here}

{phang}
Analyze your current dataset:
{cmd:. statai analyze}

{phang}
Interpret summary statistics in APA style:
{cmd:. summarize popgrowth lexp gnppc safewater}
{cmd:. statai interpret}

{title:Remarks}

{pstd}
The plugin requires an active internet connection and a valid DeepSeek API key to function.
The API key is stored securely in your Stata personal directory.

{pstd}
The analysis is performed on a preview of your data (first 10 rows) to ensure efficient processing
and to avoid sending large datasets to the API.

{pstd}
The interpret command is designed to work with the output of Stata's summary statistics commands,
particularly {cmd:summarize}. It will provide an APA-style interpretation of the descriptive statistics,
including means, standard deviations, and ranges.

{title:Author}

{pstd}
Your Name

{title:Also see}

{pstd}
For more information about the DeepSeek API, visit {browse "https://deepseek.com"} 
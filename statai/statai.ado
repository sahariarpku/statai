*! statai v1.4 - DeepSeek API integration for Stata
*! Fixed prompt handling for robust analysis
*! Author : Md Sahariar Rahman
*! Affiliation: 	Peking University
*! E-mail: 		sahariar@stu.pku.edu.cn
*! Date: 2024-12-20

program define statai
    version 16.0
    
    if "`0'" == "" {
        statai_help
        exit 0
    }
    
    gettoken subcommand rest : 0
    
    if "`subcommand'" == "setkey" {
        statai_setkey `rest'
    }
    else if "`subcommand'" == "analyze" {
        statai_analyze, prompt(`rest')
    }
    else if "`subcommand'" == "interpret" {
        statai_interpret
    }
    else if "`subcommand'" == "help" {
        statai_help
    }
    else {
        // Treat as analyze request if no recognized subcommand
        statai_analyze, prompt(`0')
    }
end

program define statai_help
    display as text _n "statai - DeepSeek API integration for Stata" _n
    display as text "Basic usage:"
    display as text "  statai setkey <api_key>     - Set your DeepSeek API key"
    display as text "  statai analyze              - General analysis of all variables"
    display as text "  statai 'analyze'    - Specific analysis request"
    display as text "  statai interpret            - Interpret last summary statistics in APA style"
    display as text "  statai help                 - Show this help message" _n
    
    display as text "Examples:"
    display as text "  . statai setkey your-api-key-here"
    display as text "  . statai analyze"
    display as text "  . statai analyze 'what kind of regression can I do here?'
    display as text "  . summarize popgrowth lexp gnppc"
    display as text "  . statai interpret" _n
    
    display as text "Notes:"
    display as text "  - You need to set your API key before using other commands"
    display as text "  - The analyze command works with your current dataset"
    display as text "  - The interpret command works with the last summary statistics"
    display as text "  - Make sure you have an active internet connection" _n
    
    display as text "For more information, type: help statai"
end

program define statai_setkey
    version 16.0
    syntax anything(name=apikey)
    
    if "`apikey'" == "" {
        display as error "API key is required"
        display as text "Usage: statai setkey your_deepseek_api_key"
        exit 198
    }
    
    global DEEPSEEK_API_KEY "`apikey'"
    
    local config_file "`c(sysdir_personal)'statai_config.txt"
    capture mkdir "`c(sysdir_personal)'"
    capture file close config
    file open config using "`config_file'", write replace
    file write config "DEEPSEEK_API_KEY=`apikey'" _n
    file close config
    
    display as text "DeepSeek API key has been set successfully"
    display as text "Config saved to: `config_file'"
end

program define statai_analyze
    version 16.0
    syntax [, prompt(string)]
    
    // Check if dataset is loaded
    quietly count
    if r(N) == 0 {
        display as error "No dataset loaded. Please load data first using 'use' or 'import'"
        exit 198
    }
    
    // Check API key
    local api_key_found = 0
    if "$DEEPSEEK_API_KEY" != "" {
        local api_key_found = 1
    }
    else {
        local config_file "`c(sysdir_personal)'statai_config.txt"
        capture confirm file "`config_file'"
        if _rc == 0 {
            local api_key_found = 1
        }
    }
    if !`api_key_found' {
        display as error "API key not set. Use 'statai setkey your_api_key' to set your API key"
        exit 198
    }
    
    // Create tmp directory if it doesn't exist
    capture mkdir tmp
    
    // Get variable information
    quietly {
        ds
        local varlist `r(varlist)'
        tempfile vars_file
        file open vars using "`vars_file'", write replace
        foreach var of local varlist {
            local vartype : type `var'
            local varformat : format `var'
            local varlabel : variable label `var'
            if "`varlabel'" != "" {
                file write vars "`var' (`vartype', `varformat') - `varlabel'" _n
            }
            else {
                file write vars "`var' (`vartype', `varformat')" _n
            }
        }
        file close vars
    }
    
    // Locate Python script
    local script_path "`c(sysdir_personal)'statai/statai_analyze.py"
    capture confirm file "`script_path'"
    if _rc != 0 {
        local script_path "`c(sysdir_plus)'statai/statai_analyze.py"
        capture confirm file "`script_path'"
        if _rc != 0 {
            // Try current directory
            local script_path "statai/statai_analyze.py"
            capture confirm file "`script_path'"
            if _rc != 0 {
                display as error "Python script 'statai_analyze.py' not found"
                display as text "Searched in:"
                display as text "1. `c(sysdir_personal)'statai/statai_analyze.py"
                display as text "2. `c(sysdir_plus)'statai/statai_analyze.py"
                display as text "3. statai/statai_analyze.py"
                display as text "Please ensure the script is installed correctly"
                exit 198
            }
        }
    }
    
    display as text "Using script: `script_path'"
    
    if "`prompt'" == "" {
        // General analysis
        display as text "Analyzing dataset variables..."
        shell python3 "`script_path'" "`vars_file'"
    }
    else {
        // Specific analysis with prompt
        tempfile promptfile
        file open prompthandle using "`promptfile'", write replace
        file write prompthandle "`prompt'"
        file close prompthandle
        display as text "Processing specific analysis request: `prompt'"
        shell python3 "`script_path'" "`promptfile'" "`vars_file'"
    }
end

program define statai_interpret
    version 16.0
    
    // Check if dataset is loaded
    quietly count
    if r(N) == 0 {
        display as error "No dataset loaded. Please load data first using 'use' or 'import'"
        exit 198
    }
    
    // Check API key
    local api_key_found = 0
    if "$DEEPSEEK_API_KEY" != "" {
        local api_key_found = 1
    }
    else {
        local config_file "`c(sysdir_personal)'statai_config.txt"
        capture confirm file "`config_file'"
        if _rc == 0 {
            local api_key_found = 1
        }
    }
    if !`api_key_found' {
        display as error "API key not set. Use 'statai setkey your_api_key' to set your API key"
        exit 198
    }
    
    // Create tmp directory
    capture mkdir tmp
    
    // Get variable information
    quietly {
        ds
        local varlist `r(varlist)'
        file open vars using "tmp/vars.txt", write replace
        foreach var of local varlist {
            local vartype : type `var'
            local varformat : format `var'
            local varlabel : variable label `var'
            if "`varlabel'" != "" {
                file write vars "`var' (`vartype', `varformat') - `varlabel'" _n
            }
            else {
                file write vars "`var' (`vartype', `varformat')" _n
            }
        }
        file close vars
    }
    
    // Save summary statistics to a file
    tempfile summary_file
    file open summary using "`summary_file'", write replace
    file write summary "Variable | Obs | Mean | Std. Dev. | Min | Max" _n
    file write summary "---------|-----|------|-----------|-----|-----" _n
    
    foreach var of local varlist {
        quietly summarize `var'
        file write summary "`var' | `r(N)' | `r(mean)' | `r(sd)' | `r(min)' | `r(max)'" _n
    }
    file close summary
    
    // Locate Python script
    local script_path "`c(sysdir_plus)'statai/statai_interpret.py"
    capture confirm file "`script_path'"
    if _rc != 0 {
        local script_path "`c(pwd)'/statai/statai_interpret.py"
        capture confirm file "`script_path'"
        if _rc != 0 {
            display as error "Python script 'statai_interpret.py' not found"
            display as text "Searched in:"
            display as text "1. `c(sysdir_plus)'statai/statai_interpret.py"
            display as text "2. `c(pwd)'/statai/statai_interpret.py"
            display as text "Please ensure the script is installed correctly"
            exit 198
        }
    }
    
    display as text "Using script: `script_path'"
    
    display as text "Interpreting summary statistics in APA style..."
    shell python3 "`script_path'" "`summary_file'" "tmp/vars.txt"
end
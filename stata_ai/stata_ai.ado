*! stata_ai v1.0.0
*! Author: Your Name
*! Date: 2024

program define stata_ai
    version 17
    syntax anything(name=prompt)
    
    * Get the current dataset path
    local data_path = "`c(filename)'"
    
    * Check if we have a dataset loaded
    if "`data_path'" == "" {
        display as error "No dataset loaded. Please load a dataset first."
        exit 198
    }
    
    * Call the Python script with the virtual environment Python
    shell stata_env/bin/python stata_ai.py "`data_path'" "`prompt'"
    
    * Display the result
    display as text "Suggested Stata command:"
    display as result "`r(command)'"
end 
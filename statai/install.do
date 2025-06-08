*! statai v1.4 - Installation script
*! Author: Md Sahariar Rahman
*! Affiliation: Peking University
*! Date: 2024-03-20

capture program drop statai
capture program drop statai_help
capture program drop statai_setkey
capture program drop statai_analyze
capture program drop statai_interpret

* Get the current directory
local current_dir "`c(pwd)'"

* Install the package
net install statai, from("`current_dir'") replace

* Make Python scripts executable
if "`c(os)'" == "Unix" {
    shell chmod +x "`current_dir'/statai_analyze.py"
    shell chmod +x "`current_dir'/statai_interpret.py"
    shell chmod +x "`current_dir'/statai_chat.py"
}

* Display success message
display as text _n "statai package has been successfully installed!" _n
display as text "To get started, type: statai help" _n
display as text "Don't forget to set your API key using: statai setkey your-api-key-here" _n 
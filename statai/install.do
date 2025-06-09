*! statai v1.4 - Installation script
*! Author: Md Sahariar Rahman
*! Affiliation: Peking University
*! Date: 2024-03-20

capture mkdir "`c(sysdir_personal)'statai"
copy statai.ado "`c(sysdir_personal)'statai/statai.ado", replace
copy statai.sthlp "`c(sysdir_personal)'statai/statai.sthlp", replace
copy statai_analyze.py "`c(sysdir_personal)'statai/statai_analyze.py", replace
copy statai_interpret.py "`c(sysdir_personal)'statai/statai_interpret.py", replace
copy statai_chat.py "`c(sysdir_personal)'statai/statai_chat.py", replace

display as text _n "statai has been installed successfully!" _n
display as text "To get started, type: statai help" 
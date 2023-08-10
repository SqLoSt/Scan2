#!/bin/bash

echo -e "\033[91m" " __         ___            ____  " "\033[0m"
echo -e "\033[91m" "/ _\       / __\__ _ _ __ |___ \ " "\033[0m"
echo -e "\033[31m" "\ \ _____ / /  / _  | '_ \  __) |" "\033[0m"
echo -e "\033[31;2m" "_\ \_____/ /__| (_| | | | |/ __/" "\033[0m"
echo -e "\033[31;2m" "\__/     \____/\__,_|_| |_|_____| [CODEBREAKERS]\n" "\033[0m"
echo -e "\033[1;31;40mS-can2.py | Professional Security Osint tool for Codebreakers Community.\n"
echo -e "\033[1;36;40mCoded by SqLoSt / https://github.com/SqLoSt\n"

read -p "$(echo -e '\033[91m' '[ ! ] Do you want to install required libraries for the tool, otherwise it won'\''t work (Y/N): ' "\033[0m")" answer

if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
    pip install requests==2.26.0 beautifulsoup4==4.9.3
    echo -e "\033[92m" "[+] Required libraries installed successfully." "\033[0m"
else
    echo -e "\033[91m" "[-] You chose not to install required libraries. The tool might not work correctly." "\033[0m"
fi

read -p "$(echo -e '\033[91m' '[?] Do you want to start S-can2.py (Y/N): ' "\033[0m")" answer

if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
    python S-can2.py
else
    echo -e "\033[91m" "All right, see you!" "\033[0m"
fi

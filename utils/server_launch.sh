#!/bin/bash

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_RESET='\033[0m'  # reset color

echo "   _____                  ____   _____"
echo "  / ____|                / __ \ / ____|"
echo " | |     _ __ ___  _ __ | |  | | (___"
echo " | |    | '__/ _ \| '_ \| |  | |\___ \\"
echo " | |____| | | (_) | | | | |__| |____) |"
echo "  \_____|_|  \___/|_| |_|\____/|_____/"

#function to run the script after a delay of 5 seconds
run_after_delay() {
    echo ""
    for ((i = 5; i >= 1; i--)); do
        echo -e "${COLOR_GREEN}Relaunch in $i secondes...${COLOR_RESET}"
        sleep 1
    done

    source ../.venv/bin/activate
    echo -e "\n${COLOR_YELLOW}==============================${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}==         Check DB         ==${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}==============================${COLOR_RESET}"
    bash ./create_cronos_db.sh
    echo -e "\n${COLOR_YELLOW}==============================${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}==          Migrate         ==${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}==============================${COLOR_RESET}"
    python ../Cronos_server/manage.py makemigrations
    python ../Cronos_server/manage.py migrate
    echo -e "\n${COLOR_YELLOW}==============================${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}==      Launch server       ==${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}==============================${COLOR_RESET}"
    python ../Cronos_server/manage.py runserver
}

# check if the argument "auto" has been passed as a parameter
if [[ "$1" == "auto" ]]; then
    while true; do
        run_after_delay
    done
else
    run_after_delay
fi

#!/bin/bash

backup_dir="$HOME/Bureau/Portfolio/backup"
backup_file="$backup_dir/Cronos_backup.sql"
CNF="$HOME/Bureau/Portfolio/.my.cnf"

# check if the backup directory exists, create it if it doesn't
if [ ! -d "$backup_dir" ]; then
    mkdir -p "$backup_dir"
fi

# save the database using the .my.cnf file
mysqldump --defaults-file="$CNF" "$DB_NAME" >"$backup_file"

#check if the backup was successful
if [ $? -eq 0 ]; then
    echo "Database backup created successfully."
else
    echo "Error creating database backup."
fi

# remove old logs using the .my.cnf file
mysql --defaults-file="$CNF" -D "$DB_NAME" -e "DELETE FROM $DB_LOGS_TABLE WHERE create_date < NOW() - INTERVAL 30 DAY;"

# check if the deletion was successful
if [ $? -eq 0 ]; then
    echo "Old logs deleted successfully."
else
    echo "Error deleting old logs."
fi

#!/bin/bash

MYSQL_CONFIG_FILE="../.my.cnf"

# If DB already exist, skip creation
if mysql --defaults-file="$MYSQL_CONFIG_FILE" -e "USE cronos"; then
  echo -e "'cronos' db already exist...\n...skipping creation."

# Create DB if not exist
else
  mysql --defaults-file="$MYSQL_CONFIG_FILE" -e "CREATE DATABASE cronos;"
  echo "'cronos' db created."
fi

exit

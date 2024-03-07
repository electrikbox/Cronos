#!/bin/bash

MYSQL_CONFIG_FILE="../../.my.cnf"

if mysql --defaults-file="$MYSQL_CONFIG_FILE" -e "USE cronos"; then
  echo -e "'cronos' db already exist...\n...skipping creation."
else
  mysql --defaults-file="$MYSQL_CONFIG_FILE" -e "CREATE DATABASE cronos;"
  echo "'cronos' db created."
fi

exit

#!/usr/bin/env bash

# Create secrets directory
mkdir secrets &> /dev/null

# Read user input
read -p "Enter database name: " database_db
read -p "Enter user: " database_user
read -s -p "Enter password: " database_password
echo ''
read -p "Enter email address: " email_address
read -s -p "Enter email password: " email_password
echo ''
read -p "Enter jwt key: " auth_jwt_key
read -p "Enter Google Maps API key: " google_maps_api_key

# Create secret files
echo $database_db > secrets/database_db
echo $database_user > secrets/database_user
echo $database_password > secrets/database_password
echo $email_address > secrets/email_address
echo $email_password > secrets/email_password
echo $auth_jwt_key > secrets/auth_jwt_key

# Replace google maps key in docker-compose file
sed -i '' 's/<REPLACE WITH KEY>/'"$google_maps_api_key"'/g' docker-compose.yml

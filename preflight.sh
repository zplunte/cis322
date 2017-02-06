#!/usr/bin/bash
# A preconfiguration script for the LOST web application
# Relies on the functionality of sql/import_data.sh

# First arg is database path
DATABASE=$1

# Create necessary LOST database tables
psql $DATABASE -f ./sql/create_tables.sql

# Retrieve LOST legacy data
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
tar -xzf osnap_legacy.tar.gz

# Import LOST legacy data into the database
bash ./sql/import_data.sh $DATABASE 5432

# Remove now unecessary legacy files
rm -rf .sql/osnap_legacy ./sql/osnap_legacy.tar.gz

# Copy source files into wsgi (will overwrite any existing index.html)
cp -R ./src/* $HOME/wsgi

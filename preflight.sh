#!/usr/bin/bash
# A preconfiguration script for the LOST web application
# Relies on the functionality of sql/import_data.sh

# First arg is database path
DATABASE=$1

# Import LOST data into database
./sql/import_data.sh $DATABASE 5432

# Copy source files into wsgi
cp -R ./src/* $HOME/wsgi

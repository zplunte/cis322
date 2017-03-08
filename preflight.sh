#!/usr/bin/bash
# A preconfiguration script for the LOST web application

# 1st arg is database path
DATABASE=$1

# Create necessary LOST database tables
psql $DATABASE -f ./sql/create_tables.sql

# Copy source files into wsgi (will overwrite any existing index.html)
cp -R ./src/* $HOME/wsgi

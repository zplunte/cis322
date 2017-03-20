#!/usr/bin/bash

DATABASE=$1

# Download LOST sample data to import 
curl -o lost_data.tar.gz https://classes.cs.uoregon.edu//17W/cis322/files/lost_data.tar.gz

# Extract LOST sample data
gzip -d lost_data.tar.gz
tar xvf lost_data.tar

# Attempt to import LOST data
./import_data.sh $DATABASE lost_data

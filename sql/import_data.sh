#!/usr/bin/env bash
# A bash script that migrates the OSNAP legacy data into a specified db
# Takes two arguments: the database name, and a port number
# Initially written by Z.P.L. for OSNAP LOST data migration.

# store first arg, should be the name of a database
DB_NAME=$1

# store second arg, should be a port number
PORT_NUM=$2

# download the legacy files with curl
curl -o osnap_legacy.tar.gz 'https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz'

# extract the legacy files
gzip -d osnap_legacy.tar.gz
tar -xvf osnap_legacy.tar

# create necessary database tables
./create_tables.sh $DB_NAME

# ---- IMPORT ASSET DATA ---- 

# py script generates sql insert script for asset legacy data
python3 gen_asset_inserts.py > tmp.sql

# run sql script to insert asset legacy data into db, store output in temporary map file
psql $DB_NAME -p $PORT_NUM -f tmp.sql > map.txt

# ---- IMPORT USER DATA ----

# py script generates sql insert script for user legacy data
python3 gen_user_inserts.py > tmp.sql

# run sql script to insert user legacy data into db, store output in temporary map file
psql $DB_NAME -p $PORT_NUM -f tmp.sql > map.txt

# ---- IMPORT SECURITY DATA ----

# py script generates sql insert script for security legacy data
python3 gen_security_inserts.py > tmp.sql

# run sql script to insert security legacy data into db, store output in temporary map file
psql $DB_NAME -p $PORT_NUM -f tmp.sql > map.txt

# clean up all temporary files
rm tmp.sql map.txt

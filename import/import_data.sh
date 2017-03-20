#!/usr/bin/bash
# Import script for importing .csv files into the LOST web application database

if [ "$#" -ne 2 ]; then
    echo "usage: ./export_data.sh <dbname> <input_dir>"
    exit;
fi

# 1st arg is database name
DATABASE=$1

# 2nd arg is input directory path
INPDIR=$2

# Make $INPDIR a full path if not already
if [[ $INPDIR != /* ]]; then
    pref=$(pwd)
    INPDIR="$pref/$INPDIR"
fi

# Remove any single trailing / from $INPDIR
if [[ $INPDIR == */ ]]; then
    INPDIR=${INPDIR%?}
fi

# If INPDIR does not exist
if [ ! -d "$INPDIR" ]; then
    echo "error: no such input directory"
    exit;
fi

# If INPDIR is not empty
if [ "$(ls -A $INPDIR)" ]; then

    # For each file in the input directory
    for filename in $INPDIR/*.csv; do

        # Check if the file is users.csv, if so import
        if [[ $filename == */users.csv ]]; then
            ./import_users.py $DATABASE $filename
        fi

        # Check if the file is assets.csv, if so import
        if [[ $filename == */assets.csv ]]; then
            ./import_assets.py $DATABASE $filename
        fi

        # Check if the file is facilities.csv, if so import
        if [[ $filename == */facilities.csv ]]; then
            ./import_facilities.py $DATABASE $filename
        fi

        # Check if the file is transfers.csv, if so import
        if [[ $filename == */transfers.csv ]]; then
            ./import_transfers.py $DATABASE $filename
        fi
    done 
else
    echo "error: no recognized files in input directory."
    echo "note: looking for files users.csv, assets.csv, facilities.csv, transfers.csv"
    exit;
fi

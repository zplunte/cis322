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

# If INPDIR does not exist
if [ ! -d "$INPDIR" ]; then
    echo "error: no such input directory"
    exit;
fi

# If INPDIR is not empty
if [ "$(ls -A $INPDIR)" ]; then
    for filename in $INPDIR/*.csv; do
        tablename="${filename#*$INPDIR/}"
        tablename="${tablename%.*}"
        ./import_csv.py $DATABASE "$tablename" "$filename"
    done 
else
    echo "error: no files in input directory"
    exit;
fi

#!/usr/bin/bash
# Export script for retrieving .csv files from LOST web application database

if [ "$#" -ne 2 ]; then
    echo "usage: ./export_data.sh <dbname> <output_dir>"
    exit;
fi

# 1st arg is database name
DATABASE=$1

# 2nd arg is output directory path
OUTDIR=$2

# If OUTDIR does not exist
if [ ! -d "$OUTDIR" ]; then
    mkdir $OUTDIR
fi

# If OUTDIR is not empty
if [ "$(ls -A $OUTDIR)" ]; then

   # Remove existing files
   rm $OUTDIR/*
fi

# Export user data to $OUTDIR/users.csv using python script
./export_users.py $DATABASE $OUTDIR

# Export facilities data to $OUTDIR/facilities.csv using python script
# ./export_facilities.py $DATABASE $OUTDIR

# Export assets data to $OUTDIR/assets.csv using python script
# ./export_assets.py $DATABASE $OUTDIR
 
# Export transfers data to $OUTDIR/transfer.csv using python script
# ./export_transfers.py $DATABASE $OUTDIR

import_data.sh

    - Bash script that takes <dbname> as 1st arg and <input_dir> as 2nd arg.
      Imports all recognized .csv files in the input directory into the sepcified
      database.

import_users.py

    - Python script that takes <dbname> as 1st arg and <filename> as 2nd arg.
      Assumes <filename> is the full path to users.csv file, and that the 
      users.csv file is properly formatted. Imports the data in the .csv file
      to the specified database.

import_assets.py

    - Python script that takes <dbname> as 1st arg and <filename> as 2nd arg.
      Assumes <filename> is the full path to assets.csv file, and that the 
      assets.csv file is properly formatted. Imports the data in the .csv file
      to the specified database.

import_facilities.py

    - Python script that takes <dbname> as 1st arg and <filename> as 2nd arg.
      Assumes <filename> is the full path to facilities.csv file, and that the 
      facilities.csv file is properly formatted. Imports the data in the .csv file
      to the specified database.

import_transfers.py

    - Python script that takes <dbname> as 1st arg and <filename> as 2nd arg.
      Assumes <filename> is the full path to transfers.csv file, and that the 
      transfers.csv file is properly formatted. Imports the data in the .csv file
      to the specified database.

test_import.sh

    - Bash script that takes <dbname> as 1st arg. Attempts to import sample LOST
      data .csv files downloaded using curl into the specified database. Utilizes 
      import_data.sh with <dbname> and the directory downloaded with curl as args.

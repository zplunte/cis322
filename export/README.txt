export_data.sh

    - Bash script to be run with <dbname> and 1st arg and <output dir> as 2nd arg.
      Exports appropriate .csv files from <dbname> to the directory <output dir>.
      If <output dir> does not exist export_data.sh creates the directory. If the 
      directory does exist, the contents are removed prior to generating the 
      export files. Calls each following python script.

export_assets.py

    - Python script that generates a .csv file from the assets table in the 
      specified database. Creates the file: assets.csv

export_facilities.py

    - Python script that generates a .csv file from the facilities table in the 
      specified database. Creates the file: facilities.csv

export_transfers.py

    - Python script that generates a .csv file from the transfers table in the
      specified database. Creates the file: transfers.csv

export_users.py

    - Python script that generates a .csv file from the users table in the
      specified database. Creates the file: users.csv

export_data.sh

    - Bash script to be run with <dbname> and 1st arg and <output dir> as 2nd arg.
      Exports appropriate .csv files from <dbname> to the directory <output dir>.
      If <output dir> does not exist export_data.sh creates the directory. If the 
      directory does exist, the contents are removed prior to generating the 
      export files.

      Creates the following export files:
      
      users.csv
      facilities.csv
      assets.csv
      transfers.csv

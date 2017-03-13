import_data.sh

    - Bash script that takes <dbname> as 1st arg and <input_dir> as 2nd arg.
      Imports all present .csv files in the input directory into the sepcified
      database.

      NOTE: <input_dir> must be the FULL path name to a directory, and it should 
            not end with '/'

import_csv.py

    - Python script takes <dbname> as 1st arg <tablename> as 2nd arg <full_path> 
      as 3rd arg. Imports the present .csv file specified by full_path into the 
      specified database.

      NOTE: I'm having trouble handling NULL's in imported .csv's using the 
            copy method. Not quite sure how to resolve this an unfortunately 
            I didn't figure it out in time. Working to resolve this as soon 
            as possible.

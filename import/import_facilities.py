#!/usr/bin/env python3

import argparse
import psycopg2 as psycop
import psycopg2.extras

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dbname', type=str)
    parser.add_argument('filename', type=str)
    args = parser.parse_args()
    dbname = args.dbname
    filename = args.filename

    connection = psycop.connect(database=dbname, host="/tmp", port="5432")
    curs = connection.cursor()

    # Read facilities.csv file, import each row
    with open(filename, "r") as f:
        lines = f.readlines();
        f.close()

    # For each row in users
    for line in lines[1:]:

        # Get each value in row
        split_line = line.split(",")
        fcode = split_line[0]
        common_name = split_line[1]

        # Insert row into facilities table (should never have to handle null values)
        curs.execute("insert into facilities (fcode, common_name) values ('{}', '{}')".format(fcode, common_name))
        
        # Commit the insert
        connection.commit()

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

    # Read users.csv file, import each row
    with open(filename, "r") as f:
        lines = f.readlines();
        f.close()

    # For each row in users
    for line in lines[1:]:

        # Get each value in row
        split_line = line.split(",")
        username = split_line[0]
        password = split_line[1]
        role = split_line[2]
        active = split_line[3]

        # Insert row into users table (should never have to handle null values)
        curs.execute("insert into users (username, password, role, active) values ('{}', '{}', '{}', '{}')".format(username, password, role, active))

        # Commit the insert
        connection.commit()

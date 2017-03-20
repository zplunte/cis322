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

    # Read transfers.csv file, import each row
    with open(filename, "r") as f:
        lines = f.readlines();
        f.close()

    # For each row in assets
    for line in lines[1:]:

        # Get each value in row
        split_line = line.split(",")
        asset_tag = split_line[0]
        request_by = split_line[1]
        request_dt = split_line[2]
        approve_by = split_line[3]
        approve_dt = split_line[4]
        source = split_line[5]
        destination = split_line[6]
        load_dt = split_line[7]
        unload_dt = split_line[8]

        if approve_by == "NULL" and load_dt == "NULL" and unload_dt == "NULL":
            
            # Insert row into transfers table without approve_by, approve_dt, load_dt, unload_dt
            curs.execute("insert into transfers (request_by, request_dt, asset_tag, source, destination) values ('{}', '{}', '{}', '{}', '{}')".format(request_by, request_dt, asset_tag, source, destination))

        elif load_dt == "NULL" and unload_dt == "NULL":

            # Insert row into transfers table with approve_by and approve_dt, but without load_dt, unload_dt
            curs.execute("insert into transfers (request_by, request_dt, approve_by, approve_dt, asset_tag, source, destination) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(request_by, request_dt, approve_by, approve_dt, asset_tag, source, destination))

        elif unload_dt == "NULL":

            # Insert row into transfers table with approve_by and approve_dt and load_dt, but without unload_dt
            curs.execute("insert into transfers (request_by, request_dt, approve_by, approve_dt, asset_tag, source, destination, load_dt) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(request_by, request_dt, approve_by, approve_dt, asset_tag, source, destination, load_dt))

        elif load_dt == "NULL":
            
            # Insert row into transfers table with approve_by and approve_dt and unload_dt, but without load_dt
            curs.execute("insert into transfers (request_by, request_dt, approve_by, approve_dt, asset_tag, source, destination, unload_dt) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(request_by, request_dt, approve_by, approve_dt, asset_tag, source, destination, unload_dt))

        else:

            # Insert row into transfers table with everything
            curs.execute("insert into transfers (request_by, request_dt, approve_by, approve_dt, asset_tag, source, destination, load_dt, unload_dt) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(request_by, request_dt, approve_by, approve_dt, asset_tag, source, destination, load_dt, unload_dt))

        # Commit the insert
        connection.commit()

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

    # Read assets.csv file, import each row
    with open(filename, "r") as f:
        lines = f.readlines();
        f.close()

    # For each row in assets
    for line in lines[1:]:

        # Get each value in row
        split_line = line.split(",")
        asset_tag = split_line[0]
        description = split_line[1]
        facility = split_line[2]
        acquired = split_line[3]
        disposed = split_line[4]

        if acquired == "NULL" or acquired == "NULL\n":

            # Insert row into assets table without acquired or disposed inserts
            curs.execute("insert into assets (asset_tag, description, facility) values ('{}', '{}', '{}')".format(asset_tag, description, facility))

        elif disposed == "NULL" or disposed == "NULL\n":

            # Insert row into assets table with acquired but without disposed insert
            curs.execute("insert into assets (asset_tag, description, facility, acquired) values ('{}', '{}', '{}', '{}')".format(asset_tag, description, facility, acquired))

        else:

            # Insert row into assets table with acquired and disposed inserts
            curs.execute("insert into assets (asset_tag, description, facility, acquired, disposed) values ('{}', '{}', '{}', '{}', '{}')".format(asset_tag, description, facility, acquired, disposed))

        # Commit the insert
        connection.commit()

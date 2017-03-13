#!/usr/bin/env python3

import argparse
import psycopg2 as psycop
import psycopg2.extras

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dbname', type=str)
    parser.add_argument('tablename', type=str)
    parser.add_argument('fullfile', type=str)
    args = parser.parse_args()
    dbname = args.dbname
    tablename  = args.tablename
    fullfile = args.fullfile

    connection = psycop.connect(database=dbname, host="/tmp", port="5432")
    curs = connection.cursor()

    # Import data
    curs.execute("copy {} from '{}' delimiter ',' csv header".format(tablename, fullfile))

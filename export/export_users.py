#!/usr/bin/env python3

import argparse
import psycopg2 as psycop
import psycopg2.extras

def make_csv(query, path, curs):
    curs.execute("copy ({}) to '{}' delimiter ',' csv header".format(query, path))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dbname', type=str)
    parser.add_argument('outdir', type=str)
    args = parser.parse_args()
    outdir  = args.outdir
    dbname = args.dbname

    connection = psycop.connect(database=dbname, host="/tmp", port="5432")
    curs = connection.cursor()

    query = """select username, password, role, active from users"""
    make_csv(query, outdir+"/users.csv", curs)

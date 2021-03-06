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

    query = """select asset_tag, description, facility, acquired, disposed from assets"""
    make_csv(query, outdir+"/assets.csv", curs)

    with open(outdir+"/assets.csv", "r") as f:
        lines = f.readlines();
        f.close()

    with open(outdir+"/assets.csv", "w") as f:
        for line in lines:
            if ",," in line:
                line = line.replace(",,", ",NULL,")
            if ",\n" in line:
                line = line.replace(",\n", ",NULL\n")
            if line[0] == ",":
                line = "NULL" + line
            f.write(line)
        f.close()

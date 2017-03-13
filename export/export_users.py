import psycopg2 as psycop
import psycopg2.extras

def make_csv(query, path, curs):
    curs.execute("copy ({}) to '{}' delimiter ',' csv header".format(query, path))

if __name__ == '__main__':

    dbname = sys.argv[1]
    outdir = sys.argv[2]

    connection = psycop.connect(database=dbname, host="\tmp", port="5432")
    curs = connection.cursor()

    query = """select username, password, role, active from userdata"""
    make_csv(query, outdir+"users.csv", curs)

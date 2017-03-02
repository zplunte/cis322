from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import psycopg2 as psycop
import psycopg2.extras
import sys
import json

# ==== INITIAL CONFIGURATION ==== #

app = Flask(__name__)

app.config['DB_NAME'] = dbname
app.config['DB_PORT'] = dbport
app.config['DB_HOST'] = dbhost

# Define secret key for session functionality
app.secret_key = "A*3&@71j/018jfdsAJI17fds81#@1"

# Connect to psycopg2 as 'psycop' and get cursor as 'curs'
connection = psycop.connect(database=dbname, host=dbhost, port=dbport)
curs = connection.cursor()

# ==== USEFUL UTILITY FUNCTIONS ==== #

# Returns the role associated with a given username uname
def get_user_role(uname):
    curs.execute("""select role from userdata where username='{}'""".format(uname))
    urole = curs.fetchone()
    return urole[0]

# Returns list of columns in assets, excluding rows where is_disposed is true
def get_asset_list():
    curs.execute("""select * from assets where is_disposed=False""")
    asset_list = curs.fetchall()
    return asset_list

# Returns list of columns in facilities
def get_facility_list():
    curs.execute("""select * from facilities""")
    facility_list = curs.fetchall()
    return facility_list

# Returns true if the username uname is in the database
def user_exists(uname):
    curs.execute("""select username from userdata where username='{}'""".format(uname))
    return (curs.fetchone() is not None)

# Returns true if the asset_tag atag is in the database
def asset_exists(atag):
    curs.execute("""select asset_tag from assets where asset_tag='{}'""".format(atag))
    return (curs.fetchone() is not None)

# Returns true if fname or fcode exist in database as facility common_name or code
def facility_exists(fname, fcode):
    curs.execute("""select common_name from facilities where common_name='{}'""".format(fname))
    result = (curs.fetchone() is not None)
    curs.execute("""select code from facilities where code='{}'""".format(fcode))
    result = result or (curs.fetchone() is not None)
    return result

# Return asset is_disposed state
def asset_is_disposed(atag):
    curs.execute("""select is_disposed from assets where asset_tag='{}'""".format(atag))
    disposal_state = curs.fetchone()
    if disposal_state != None:
        return disposal_state[0]
    return None

# ==== ROUTES ==== #

# Default page, prompts user login / user creation
@app.route('/', methods=(['GET', 'POST']))
@app.route('/index', methods=(['GET', 'POST']))
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        if 'password' in request.form and 'username' in request.form:
            uname = request.form['username']
            if user_exists(uname):
                session['username'] = uname
                session['role'] = get_user_role(uname)
                passwd = request.form['password']
                curs.execute("""select password from userdata where username='{}'""".format(uname))
                if curs.fetchone()[0] == passwd:
                    return dashboard()
        return render_template('invalid_login.html')
    return render_template('invalid_login.html')

@app.route('/create_user', methods=(['POST', 'GET']))
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'role' in request.form:
            uname = request.form['username']
            if user_exists(uname):
                return render_template('user_exists.html')
            else:
                urole = request.form['role']
                upass = request.form['password']
                curs.execute("""insert into userdata (username, password, role) values ('{}', '{}', '{}')""".format(uname, upass, urole))
                connection.commit()
                return render_template('user_created.html')
        return render_template('create_user.html')

@app.route('/dashboard', methods=(['GET']))
def dashboard():
    if 'username' in session and 'role' in session:
        return render_template('dashboard.html', username = session['username'], role = session['role'])

@app.route('/add_facility', methods=(['GET', 'POST']))
def add_facility():
    if request.method == 'GET':
        facility_list = get_facility_list()
        return render_template('add_facility.html', facilities = facility_list)
    if request.method == 'POST':
        if 'facility_common_name' in request.form and 'facility_code' in request.form:
            fname = request.form['facility_common_name']
            fcode = request.form['facility_code']
            if facility_exists(fname, fcode):
                return render_template('facility_exists.html')
            else: 
                curs.execute("""insert into facilities (common_name, code) values ('{}', '{}')""".format(fname, fcode))
                connection.commit()
                return render_template('facility_created.html')
        return render_template('add_facility.html')

@app.route('/add_asset', methods=(['GET', 'POST']))
def add_asset():
    if request.method == 'GET':
        asset_list = get_asset_list()
        facility_list = get_facility_list()
        return render_template('add_asset.html', assets = asset_list, facilities = facility_list)
    if request.method == 'POST':
        if 'asset_tag' in request.form and 'asset_description' in request.form and 'asset_facility_code' in request.form and 'asset_arrival_time' in request.form:
            atag = request.form['asset_tag']
            adesc = request.form['asset_description']
            afname = request.form['asset_facility_code']
            aarrival = request.form['asset_arrival_time']
            if asset_exists(atag):
                return render_template('asset_exists.html')
            else:
                curs.execute("""insert into assets (asset_tag, description) values ('{}', '{}')""".format(atag, adesc))
                connection.commit()
                return render_template('asset_created.html')
        return render_template('add_asset.html')

@app.route('/dispose_asset', methods=(['GET', 'POST']))
def dispose_asset():
    if request.method == 'GET':
        asset_list = get_asset_list()
        return render_template('dispose_asset.html', assets = asset_list)
    if request.method == 'POST':
        if 'role' in session and 'disposal_asset_tag' in request.form and 'disposal_time' in request.form:
            if session['role'] != "Logistics Officer":
                return render_template('invalid_role_for_disposal.html')
            datag = request.form['disposal_asset_tag']
            dtime = request.form['disposal_time']
            if asset_exists(datag):
                if (asset_is_disposed(datag)):
                    return render_template('asset_already_disposed.html')
                else:
                    curs.execute("""update assets set is_disposed=True where asset_tag='{}'""".format(datag))
                    connection.commit()
                    # need to also update disposal time
                    return render_template('asset_disposed.html')
            else:
                return render_template('asset_does_not_exist.html') 
        return render_template('dashboard.html')

def report_date(repdate):
    return render_template('asset_report.html')

def report_date_and_fac(repdate, repfac):
    return render_template('asset_report.html')

@app.route('/asset_report', methods=(['GET', 'POST']))
def asset_report():
    if request.method == 'GET':
        return render_template('asset_report.html')
    if request.method == 'POST':
        if 'report_date' in request.form:
            repdate = request.form['report_date']
            if 'report_facility' in request.form:
                repfac = request.form['report_facility']
                return report_date_and_fac(repdate, repfac)
            else:
                return report_date(repdate)
        return render_template('asset_report.html')

# ==== RUN APP ==== #

if __name__ == "__main__":
    app.run(host=dbhost, port=dbport)

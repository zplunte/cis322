from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import psycopg2 as psycop
import psycopg2.extras
import sys
import json
import datetime

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
    curs.execute("""select role from users where username='{}'""".format(uname))
    urole = curs.fetchone()
    return urole[0]

# Returns list of columns in assets
def get_asset_list():
    curs.execute("""select * from assets""")
    asset_list = curs.fetchall()
    return asset_list

# Returns list of columns in assets, excluding rows where is_disposed is true
def get_non_disposed_asset_list():
    curs.execute("""select * from assets where is_disposed=False""")
    asset_list = curs.fetchall()
    return asset_list


# Returns list of columns in joined assets and asset_position
def get_asset_list_with_position():
    curs.execute("""select assets.asset_tag, assets.description, assets.is_disposed, assets.in_transit, asset_position.arrival_time, asset_position.departure_time from assets inner join asset_position on assets.asset_tag=asset_position.a_tag""")
    asset_list = curs.fetchall()
    return asset_list

# Returns custom list of columns in facilities, for add_facility screen
def get_add_facility_data_list():
    curs.execute("""select fcode, common_name from facilities""")
    facilities_list = curs.fetchall()
    return facilities_list 

# Returns custom list of columns in joined non-disposed assets 
# and asset_position and facilities, for add/dispose_asset screens
def get_add_dispose_asset_data_list():
    curs.execute("""select assets.asset_tag, assets.description, facilities.common_name, asset_position.arrival_time from assets join asset_position on assets.asset_tag=asset_position.a_tag left join facilities on asset_position.f_code=facilities.fcode where assets.is_disposed=False""")
    asset_list = curs.fetchall()
    return asset_list

# Returns custom list of columns in joined assets and asset_position
# and facilities, for asset_report screen
def get_asset_report_data_list(test_year, test_month, test_day, test_facility_code):

    main_query = "select assets.asset_tag, assets.description, facilities.common_name, asset_position.arrival_time, asset_position.departure_time from assets join asset_position on assets.asset_tag=asset_position.a_tag left join facilities on asset_position.f_code=facilities.fcode"

    if test_facility_code == 'ALL_FACILITIES':

        if (test_year != 'none') and (test_month == 'none') and (test_day == 'none'):
            test_date_start = test_year + '-01-01'
            test_date_end = test_year + '-12-31'
            curs.execute(main_query + " where (asset_position.arrival_time >= '{0}' and asset_position.arrival_time <= '{1}') or (asset_position.departure_time >= '{0}' and asset_position.departure_time <= '{1}')".format(test_date_start, test_date_end))
            data_list = curs.fetchall()
            return data_list

        elif (test_year != 'none') and (test_month != 'none') and (test_day == 'none'):
            test_date_start = test_year + '-' + test_month + '-01'
            test_date_end = test_year + '-' + test_month + '-31'
            curs.execute(main_query + " where (asset_position.arrival_time >= '{0}' and asset_position.arrival_time <= '{1}') or (asset_position.departure_time >= '{0}' and asset_position.departure_time <= '{1}')".format(test_date_start, test_date_end))
            data_list = curs.fetchall()
            return data_list

        elif (test_year != 'none') and (test_month != 'none') and (test_day != 'none'):
            test_date = test_year + '-' + test_month + '-' + test_day
            curs.execute(main_query + " where asset_position.arrival_time = '{0}' or asset_position.departure_time = '{0}'".format(test_date))
            data_list = curs.fetchall()
            return data_list

        else:
            curs.execute(main_query)
            data_list = curs.fetchall()
            return data_list
    else:
        if (test_year != 'none') and (test_month == 'none') and (test_day == 'none'):
            test_date_start = test_year + '-01-01'
            test_date_end = test_year + '-12-31'
            curs.execute(main_query + " where (asset_position.arrival_time >= '{0}' and asset_position.arrival_time <= '{1}') or (asset_position.departure_time >= '{0}' and asset_position.departure_time <= '{1}') and facilities.fcode='{2}'".format(test_date_start, test_date_end, test_facility_code))
            data_list = curs.fetchall()
            return data_list

        elif (test_year != 'none') and (test_month != 'none') and (test_day == 'none'):
            test_date_start = test_year + '-' + test_month + '-01'
            test_date_end = test_year + '-' + test_month + '-31'
            curs.execute(main_query + " where (asset_position.arrival_time >= '{0}' and asset_position.arrival_time <= '{1}') or (asset_position.departure_time >= '{0}' and asset_position.departure_time <= '{1}') and facilities.fcode='{2}'".format(test_date_start, test_date_end, test_facility_code))
            data_list = curs.fetchall()

        elif (test_year != 'none') and (test_month != 'none') and (test_day != 'none'):
            test_date = test_year + '-' + test_month + '-' + test_day
            curs.execute(main_query + " where asset_position.arrival_time = '{0}' or asset_position.departure_time = '{0}' and facilities.fcode='{1}'".format(test_date, test_facility_code))
            data_list = curs.fetchall()
            return data_list

        else:
            curs.execute(main_query + " where facilities.fcode='{}'".format(test_facility_code))
            data_list = curs.fetchall()
            return data_list
    return

# Returns list of columns in facilities
def get_facility_list():
    curs.execute("""select * from facilities""")
    facility_list = curs.fetchall()
    return facility_list

# Returns list of columns in asset_position
def get_asset_position_list():
    curs.execute("""select * from asset_position""")
    asset_position_list = curs.fetchall()
    return asset_list

# Returns true if the username uname is in the database
def user_exists(uname):
    curs.execute("""select username from users where username='{}'""".format(uname))
    return (curs.fetchone() is not None)

# Returns true if the asset_tag atag is in the database
def asset_exists(atag):
    curs.execute("""select asset_tag from assets where asset_tag='{}'""".format(atag))
    return (curs.fetchone() is not None)

# Returns true if fname or fcode exist in database as facility common_name or code
def facility_exists(fname, fcode):
    curs.execute("""select common_name from facilities where common_name='{}'""".format(fname))
    result = (curs.fetchone() is not None)
    curs.execute("""select fcode from facilities where fcode='{}'""".format(fcode))
    result = result or (curs.fetchone() is not None)
    return result

# Return asset is_disposed state
def asset_is_disposed(atag):
    curs.execute("""select is_disposed from assets where asset_tag='{}'""".format(atag))
    disposal_state = curs.fetchone()
    if disposal_state != None:
        return disposal_state[0]
    return None

# Returns list of columns in transfers
def get_transfer_requests_needing_approval_list():
    curs.execute("select * from transfers where approve_by is null")
    asset_list = curs.fetchall()
    return asset_list

# Returns list of columns in transfers
def get_transfer_requests_needing_transit_update_list():
    curs.execute("select * from transfers where unload_dt is null")
    result = curs.fetchall()
    return result

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
                curs.execute("""select password from users where username='{}'""".format(uname))
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
                curs.execute("""insert into users (username, password, role) values ('{}', '{}', '{}')""".format(uname, upass, urole))
                connection.commit()
                return render_template('user_created.html')
        return render_template('create_user.html')

@app.route('/dashboard', methods=(['GET', 'POST']))
def dashboard():
    if 'username' in session and 'role' in session:
        if session['role'] == "Logistics Officer":
            job_list = get_transfer_requests_needing_transit_update_list()
            return render_template('logistics_dashboard.html', username = session['username'], role = session['role'], jobs = job_list)
        else:
            job_list = get_transfer_requests_needing_approval_list()
            return render_template('dashboard.html', username = session['username'], role = session['role'], jobs = job_list)

@app.route('/add_facility', methods=(['GET', 'POST']))
def add_facility():
    if request.method == 'GET':
        data_list = get_add_facility_data_list()
        return render_template('add_facility.html', data = data_list)
    if request.method == 'POST':
        if 'facility_common_name' in request.form and 'facility_code' in request.form:
            fname = request.form['facility_common_name']
            fcode = request.form['facility_code']
            if facility_exists(fname, fcode):
                return render_template('facility_exists.html')
            else: 
                curs.execute("""insert into facilities (common_name, fcode) values ('{}', '{}')""".format(fname, fcode))
                connection.commit()
                return render_template('facility_created.html')
        return render_template('add_facility.html')

@app.route('/add_asset', methods=(['GET', 'POST']))
def add_asset():

    # GET method procedure
    if request.method == 'GET':

        # Get list of rows in assets
        data_list = get_add_dispose_asset_data_list()

        # Get list of rows in facilities
        facility_list = get_facility_list()

        # Render add_asset.html, load asset_list as "assets", facility_list as "facilities"
        return render_template('add_asset.html', data = data_list, facilities = facility_list)

    # POST method procedure
    if request.method == 'POST':
        if 'asset_tag' in request.form and 'asset_description' in request.form and 'asset_facility_code' in request.form and 'asset_arrival_year' in request.form and 'asset_arrival_month' in request.form and 'asset_arrival_day' in request.form:
            a_tag = request.form['asset_tag']
            a_desc = request.form['asset_description']
            f_code = request.form['asset_facility_code']
            arr_year = request.form['asset_arrival_year']
            arr_month = request.form['asset_arrival_month']
            arr_day = request.form['asset_arrival_day']
            arr_date = arr_year + '-' + arr_month + '-' + arr_day 

            if len(a_tag) == 0:
                return render_template('empty_asset_tag.html')
            if len(a_desc) == 0:
                return render_template('empty_asset_desc.html')
            
            if asset_exists(a_tag):
                return render_template('asset_exists.html')
            else:
                curs.execute("""insert into assets (asset_tag, description, facility) values ('{}', '{}', '{}')""".format(a_tag, a_desc, f_code))
                connection.commit()
                curs.execute("""insert into asset_position (arrival_time, a_tag, f_code) values ('{}', '{}', '{}')""".format(arr_date, a_tag, f_code))
                connection.commit()
                return render_template('asset_created.html')
        return render_template('add_asset.html')

@app.route('/dispose_asset', methods=(['GET', 'POST']))
def dispose_asset():
    if request.method == 'GET':
        data_list = get_add_dispose_asset_data_list()
        return render_template('dispose_asset.html', data = data_list)
    if request.method == 'POST':
        if 'role' in session and 'disposal_asset_tag' in request.form:
            if session['role'] != "Logistics Officer":
                return render_template('invalid_role_for_disposal.html')
            datag = request.form['disposal_asset_tag']
            dis_year = request.form['asset_disposal_year']
            dis_month = request.form['asset_disposal_month']
            dis_day = request.form['asset_disposal_day']
            dis_date = dis_year + '-' + dis_month + '-' + dis_day
            if asset_exists(datag):
                if (asset_is_disposed(datag)):
                    return render_template('asset_already_disposed.html')
                else:
                    curs.execute("""update assets set is_disposed=True where asset_tag='{}'""".format(datag))
                    connection.commit()
                    curs.execute("""update asset_position set departure_time='{}' where a_tag='{}'""".format(dis_date, datag))
                    connection.commit()
                    return render_template('asset_disposed.html')
            else:
                return render_template('asset_does_not_exist.html') 
        return render_template('dashboard.html')

@app.route('/asset_report', methods=(['GET', 'POST']))
def asset_report():
    facility_list = get_facility_list()
    if request.method == 'GET':
        return render_template('asset_report.html', facilities = facility_list)
    if request.method == 'POST':
        if 'report_year' in request.form and 'report_month' in request.form and 'report_day' in request.form and 'report_facility_code' in request.form:
            rep_year = request.form['report_year']
            rep_month = request.form['report_month']
            rep_day = request.form['report_day']
            rep_f_code = request.form['report_facility_code']
            data_list = get_asset_report_data_list(rep_year, rep_month, rep_day, rep_f_code)
            return render_template('asset_report.html', data = data_list, facilities = facility_list)
        return render_template('asset_report.html')

@app.route('/tranfer_report', methods=(['GET', 'POST']))
def transfer_report():
    if request.method == 'GET':
        return render_template('transfer_report.html')
    if request.method == 'POST':
        return render_template('transfer_report.html')

@app.route('/transfer_req', methods=(['GET', 'POST']))
def transfer_req():
    if 'role' in session:
        if session['role'] != "Logistics Officer":
            return render_template('invalid_role_for_transfer_request.html')
    facility_list = get_facility_list()
    asset_list = get_non_disposed_asset_list()
    if request.method == 'GET': 
        return render_template('transfer_req.html', assets = asset_list, facilities = facility_list)
    if request.method == 'POST': 
        req_user = session['username']
        req_date = str(datetime.datetime.now().date())
        req_tag = request.form['transfer_asset_tag']
        req_src = request.form['transfer_src_facility_code']
        req_dest = request.form['transfer_dest_facility_code']
        curs.execute("insert into transfers (request_by, request_dt, asset_tag, source, destination) values ('{0}','{1}','{2}','{3}','{4}')".format(req_user, req_date, req_tag, req_src, req_dest))
        connection.commit()
        return render_template('transfer_req_completed.html')

def request_exists(test_req_pk):
    curs.execute("""select request_pk from transfers where request_pk='{}'""".format(test_req_pk))
    return (curs.fetchone() is not None)

def request_not_approved(test_req_pk):
    curs.execute("""select approve_by from transfers where request_pk='{}'""".format(test_req_pk))
    approver = curs.fetchone()
    if approver != None:
        return approver[0] == None
    return true

def get_specific_request_data(test_req_pk):
    curs.execute("""select * from transfers where request_pk='{}'""".format(test_req_pk))
    req_list = curs.fetchall()
    return req_list

def accept_transfer_request(app_user, req_for_app):
    curs.execute("""update transfers set approve_by='{}' where request_pk='{}'""".format(app_user, req_for_app))
    app_date = str(datetime.datetime.now().date())
    curs.execute("""update transfers set approve_dt='{}' where request_pk='{}'""".format(app_date, req_for_app))
    connection.commit()
    return;

def reject_transfer_request(req_for_app):
    curs.execute("""delete from transfers where request_pk='{}'""".format(req_for_app))
    connection.commit()
    return;

@app.route('/approve_req', methods=(['GET', 'POST']))
def approve_req():
    if 'role' in session:
        if session['role'] != "Facilities Officer":
            return render_template('invalid_role_for_transfer_approval.html')
    if request.method == 'GET':
        if 'req_for_approval_pk' in request.args:
            req_for_app = request.args['req_for_approval_pk']
            session['req_for_approval_pk'] = req_for_app
            if request_exists(req_for_app):
                if request_not_approved(req_for_app):
                    specific_req_data = get_specific_request_data(req_for_app)
                    return render_template('approve_req.html', req_data = specific_req_data)
                else:
                    return render_template('req_already_approved.html')
            else:
                return render_template('req_does_not_exist.html')
        return render_template('req_does_not_exist.html')
    if request.method == 'POST':
        if 'req_accept' in request.form:
            accept_transfer_request(session['username'], session['req_for_approval_pk'])
            return dashboard()
        if 'req_reject' in request.form:
            reject_transfer_request(session['req_for_approval_pk'])
            return dashboard()
        return render_template('req_does_not_exist.html')

def update_transit_load(req_pk, upd_year, upd_month, upd_day):
    upd_date = upd_year + '-' + upd_month + '-' + upd_day 
    curs.execute("""update transfers set load_dt='{}' where request_pk='{}'""".format(upd_date, req_pk))
    connection.commit()
    return;

def update_transit_unload(req_pk, upd_year, upd_month, upd_day):
    upd_date = upd_year + '-' + upd_month + '-' + upd_day
    curs.execute("""update transfers set unload_dt='{}' where request_pk='{}'""".format(upd_date, req_pk))
    connection.commit() 
    return;A

def request_not_updated(test_req_pk):
    curs.execute("""select unload_dt from transfers where request_pk='{}'""".format(test_req_pk))
    unload_date = curs.fetchone()
    if unload_date != None:
        return unload_date[0] == None
    return true

@app.route('/update_transit', methods=(['GET', 'POST']))
def update_transit():
    if 'role' in session:
        if session['role'] != "Logistics Officer":
            return render_template('invalid_role_for_transit_update.html')
    if request.method == 'GET':
        if 'req_for_transit_update_pk' in request.args:
            req_for_upd = request.args['req_for_transit_update_pk']
            session['req_for_transit_update_pk'] = req_for_upd
            if request_exists(req_for_upd):
                if request_not_updated(req_for_upd):
                    return render_template('update_transit.html')
                else:
                    return render_template('req_already_updated.html')
            else:
                return render_template('req_does_not_exist.html')
        return render_template('req_does_not_exist.html')
    if request.method == 'POST':
        if 'upd_load_year' in request.form and 'upd_load_month' in request.form and 'upd_load_day' in request.form:
            update_transit_load(session['req_for_approval_pk'], request.form['upd_load_year'], request.form['upd_load_month'], request.form['upd_load_day'])
            return dashboard()
        if 'upd_unload_year' in request.form and 'upd_unload_month' in request.form and 'upd_unload_day' in request.form:
            update_transit_unload(session['req_for_approval_pk'], request.form['upd_unload_year'], request.form['upd_unload_month'], request.form['upd_unload_day'])
            return dashboard()
        return dashboard()

@app.route('/logistics_set_load_unload', methods=(['GET', 'POST']))
def logistics_set_load_unload():
    if request.method == 'GET':
        return render_template('logistics_set_load_unload.html')
    if request.method == 'POST':
        return render_template('logistics_set_load_unload.html')

# ==== RUN APP ==== #

if __name__ == "__main__":
    app.run(host=dbhost, port=dbport)

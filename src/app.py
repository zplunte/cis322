from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import psycopg2 as psycop
import psycopg2.extras
import sys
import json

app = Flask(__name__)

app.config['DB_NAME'] = dbname
app.config['DB_PORT'] = dbport
app.config['DB_HOST'] = dbhost

connection = psycop.connect(database=dbname, host=dbhost, port=dbport)
curs = connection.cursor()

@app.route('/', methods=(['POST', 'GET']))
def home():
    return render_template('index.html')

@app.route('/index', methods=(['POST', 'GET']))
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        if 'password' in request.form and 'username' in request.form:
            uname = request.form['username']
            if user_exists(uname):
                passwd = request.form['password']
                curs.execute("""select password from userdata where username='{}'""".format(uname))
                if curs.fetchone() is not None:
                    return dashboard()
        return render_template('invalid_login.html')
    return render_template('invalid_login.html')

def user_exists(uname):
    curs.execute("""select username from userdata where username='{}'""".format(uname))
    return (curs.fetchone() is not None)

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
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return None

if __name__ == "__main__":
    app.run(host=dbhost, port=dbport)

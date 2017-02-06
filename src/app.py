from flask import Flask, render_template, request
from config import dbname, dbhost, dbport

# NOTE: Couldn't quite figure out how to include database info...
# I know I need to do something with the psql database in fir()
# and itr() below, but I can't quite figure out what. Somehow I 
# need to get the user input, call a psql query based on that 
# input, and then feed the results of the query in the HTML 
# tables. Just not sure how to do it yet and I've run out of time.
# I think I was able to provide a solid layout and screen flow though!
# It would be nice to go over some of the procedures for integrating 
# database data into pages during class sometime.

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rf', methods=['POST', 'GET'])
def rf():
    if request.method == 'POST':
        return render_template('rf.html')

@app.route('/fir', methods=['POST', 'GET'])
def fir():
    if request.method == 'POST':
        return render_template('fir.html', dbname=dbname, dbhost=dbhost, dbport=dbport)

@app.route('/itr', methods=['POST', 'GET'])
def itr():
    if request.method == 'POST':
        return render_template('itr.html', dbname=dbname, dbhost=dbhost, dbport=dbport)

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == "__main__":
    app.run()

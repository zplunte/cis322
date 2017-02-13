from flask import Flask, render_template, request
from config import dbname, dbhost, dbport
import json, datetime, time

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

@app.route('/rest')
def rest():
    return render_template('rest.html')

@app.route('/rest/lost_key', methods=(['POST']))
def lost_key():

    # Create dictionary for response data
    response_data = dict()

    # Get formatted timestamp, create key-value pair in dictionary
    timest = time.time()
    response_data["timestamp"] = datetime.datetime.fromtimestamp(timest).strftime("%Y-%m-%d %H:%M%:S")

    # Determine result
    response_data["result"] = "OK"

    # Provide LOST public key
    response_data["key"] = "key123key456key789..."

    # return response_data via json
    return json.dumps(response_data)

if __name__ == "__main__":
    app.run()

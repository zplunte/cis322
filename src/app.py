from flask import Flask, render_template, request
from config import dbname, dbhost, dbport

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

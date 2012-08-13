'# -*- coding: utf-8 -*-'
from __future__ import division

__Synopsys__    = 'Offer a HTML UI to the Opinion Calculator Web service' 
__author__      = 'Dr. Avner OTTENSOOSER'
__version__     = '$Revision: 0.01 $'
__email__       = 'avner.ottensooser@gmail.com'

AO_ROOT_PATH    = 'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_PROJECT_NAME = 'interfaces'
AO_DATABASE     = AO_ROOT_PATH + AO_PROJECT_NAME + '\\Data\\Database\\flaskr.db'

import urllib2
from suds.client import Client
try:
    AO_client = Client('http://localhost:7789/?wsdl')
except urllib2.URLError:
    print "Cannot establish connecttion with SOAP server. Please ensure that the SOAP server is running and start again."
    raise SystemExit
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

# Import the modules required by Flask
import sqlite3
from werkzeug.wrappers import Request, Response
from jinja2 import Template
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response

# configuration These variable are visible to the app object
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = '\xa5M\x05\xda=Y<\xfdV\x1f#\xa6\\\xbd%\xd8\xa1mBd\xca\xc9\xb1\xfe' # the key is generated using os.urandom(24)
app.debug = True

# this function returns a connection to the databaase
def AO_oConnect_db():
    return sqlite3.connect(app.config['AO_DATABASE'])

@app.before_request
def before_request():
    #connect to the database
    g.db = AO_oConnect_db()

@app.teardown_request
def teardown_request(exception):
    #close the database
    g.db.close()

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    # Read from the screen and store in a session variable    
    session['AO_sDocument'] = request.form['text']

    # Analyse the document by calling the Opinion Assesment web service
    AO_lOpinion=  AO_client.service.opinionAssesmentRequest(session.get('AO_sDocument'))[0]

    # Store the request and teh response in the database
    g.db.execute('insert into entries (title, text) values (?, ?)',[session.get('AO_sDocument'), AO_lOpinion[4]])
    g.db.commit()
    
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/', methods=['GET', 'POST'])
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc limit 5')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    # render_template('show_entries.html', entries=entries)
    return render_template('show_entries.html', AO_sDocument =  session.get('AO_sDocument'), entries=entries)

if __name__ == '__main__':
    app.run()

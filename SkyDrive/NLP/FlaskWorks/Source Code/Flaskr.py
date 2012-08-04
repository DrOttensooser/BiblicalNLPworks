'# -*- coding: utf-8 -*-'
from __future__ import division

''' 
        This module offers a HTML  UI to the Opinion Calculator 
'''

__author__ = 'Dr. Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

AO_ROOT_PATH         = 'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_PROJECT_NAME      = 'FlaskWorks'
AO_DATABASE          = AO_ROOT_PATH + AO_PROJECT_NAME + '\\Data\\Database\\flaskr.db'
AO_sCommonPath       =  AO_ROOT_PATH + 'CommonWorks\\'
AO_sCommonCode       =  AO_sCommonPath + 'Source Code'

# import the NLPworks opinion analuser
import sys
sys.path.append(AO_sCommonCode)
import AO_mOpinionWords

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
    session['AO_sDocument'] = request.form['text']

    # Analyse the document
    AO_lOpinion = AO_mOpinionWords.AO_lAssessOpinion(session.get('AO_sDocument'))
    AO_sOpinion = "Positive = %g, Negative = %g, Net = %g.  Reasone = %s " % (AO_lOpinion[0],AO_lOpinion[1],AO_lOpinion[2],AO_lOpinion[3])

    if AO_lOpinion[2] > 0:
        AO_stentiment = "Positive"
    elif AO_lOpinion[2] < 0:
        AO_stentiment = "Negative"
    else:
        AO_stentiment = "Nutral"

    AO_sFullOpinion = 'The overall sentiment of "%s" is: %s <%g>. The rational is: %s.' %(session.get('AO_sDocument'), AO_stentiment ,AO_lOpinion[2],AO_lOpinion[3])

    g.db.execute('insert into entries (title, text) values (?, ?)',[session.get('AO_sDocument'), AO_sFullOpinion])
    g.db.commit()
    
  
    
    # flash('The overall sentiment of "%s" is: %s <%g>. The rational is: %s.' %(session.get('AO_sDocument'), AO_stentiment ,AO_lOpinion[2],AO_lOpinion[3]))
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

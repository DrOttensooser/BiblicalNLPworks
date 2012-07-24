'# -*- coding: utf-8 -*-'
from __future__ import division

''' 
        This module offers a HTML based UI to the Opinion Calculator 
'''

__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

AO_ROOT_PATH         = 'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_PROJECT_NAME      = 'FlaskWorks'
AO_DATABASE          = AO_ROOT_PATH + AO_PROJECT_NAME + '\\Data\\Database\\flaskr.db'

import sqlite3
from werkzeug.wrappers import Request, Response
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['AO_DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',[request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
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

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)    

if __name__ == '__main__':
    app.run()

import sqlite3
from werkzeug.wrappers import Request, Response
from jinja2 import Template
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = '\xa5M\x05\xda=Y<\xfdV\x1f#\xa6\\\xbd%\xd8\xa1mBd\xca\xc9\xb1\xfe'  
app.debug = True

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    AO_sInteger = str(int(request.form['text']) + 1)
    render_template('show_entries.html', AO_sInteger = AO_sInteger)
    resp = make_response(render_template('show_entries.html', AO_sInteger = AO_sInteger))
    resp.set_cookie('AO_sInteger', AO_sInteger)
    flash('the new inteher is: %s.' %(AO_sInteger))
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('show_entries'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/', methods=['GET', 'POST'])
def show_entries():
    try:
        AO_sInteger = request.cookies.get('AO_sInteger')
        if AO_sInteger == 'None':
            AO_sInteger == '43'
    except KeyError:
        AO_sInteger = '42'
    flash(AO_sInteger)
    return render_template('show_entries.html', AO_sInteger = AO_sInteger)  

if __name__ == '__main__':
    app.run()

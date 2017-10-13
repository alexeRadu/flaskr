from __future__ import print_function
import sys, os, sqlite3
from flask import Flask, g, render_template, request, redirect, flash, url_for, session

# print to console
def cprint(msg):
	print(msg, file=sys.stderr)

# create the application instance
app = Flask(__name__)

# Load config from this file.
# This means that I can define a global variable with an all caps name and it
# will be loaded into the config
# ex. NAME = "Radu"
# For a larger application the default configuration could be stored into either
# a config.py or a config.ini file and loaded at this point.
app.config.from_object(__name__)

# Manually override default config
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
	SECRET_KEY="development key",
	USERNAME="admin",
	PASSWORD="default"
))

# Override config from environmental parameters. The variable FLASKR_SETTINGS
# should point to the configuration file.
# ex: export FLASKR_SETTINGS=config.py
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Connect to a specific database
def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

def query_db(query):
	db = get_db()
	return db.execute(query).fetchall()


@app.cli.command('initdb')
def initdb_command():
	init_db()
	cprint("Database has been initialized")

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def show_entries():
	entries = query_db('select title, text from entries order by id desc')
	return render_template('show_entries.html', entries=entries)

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
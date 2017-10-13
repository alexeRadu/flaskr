from __future__ import print_function
import sys, os
from flask import Flask

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

@app.route('/')
def hello_world():
	cprint(str(app.config))
	return "Hello there"
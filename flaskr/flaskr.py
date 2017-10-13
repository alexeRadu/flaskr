from __future__ import print_function
import sys
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

@app.route('/')
def hello_world():
	cprint(str(app.config))
	return "Hello there"
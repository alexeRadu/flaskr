from __future__ import print_function
import sys
from flask import Flask

# print to console
def cprint(msg):
	print(msg, file=sys.stderr)

# create the application instance
app = Flask(__name__)

# load config from this file
app.config.from_object(__name__)

@app.route('/')
def hello_world():
	cprint("Console messsage from %s" % ("Radu"))
	return "Hello there"
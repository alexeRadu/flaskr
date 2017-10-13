from flask import Flask

NAME = 'radu'

# create the application instance
app = Flask(__name__)

# load config from this file
app.config.from_object(__name__)

@app.route('/')
def hello_world():
	print("Hi there boy")
	return "Hello there"
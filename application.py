# located outside of the site folder
# website is now a pyton package so by default it will run anything in our init.py file
from flask import Flask
from website import create_application

application = create_application()
#application = Flask(__name__)

if __name__ == "__main__": 	# runs flask app, only if we run this file it will run the server
    application.debug = True
    application.run()

# test

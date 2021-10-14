# located outside of the site folder
from website import create_app	# website is now a pyton package so by default it will run anything in our init.py file

app = create_app()

if __name__ == "__main__": 	# runs flask app, only if we run this file it will run the server
	app.run(debug=True)	
	
#test
# located outside of the site folder
# website is now a pyton package so by default it will run anything in our init.py file
from website import create_app

app = create_app()

if __name__ == "__main__": 	# runs flask app, only if we run this file it will run the server
    app.run(debug=True)
    app.run(host='0.0.0.0')

# test

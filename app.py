from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flaskext.lesscss import lesscss
from findgoodmovies import *

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
	return "Hello world!"

@app.route('/search/<int:zipcode>/<float:imdb>/<int:metacrit>')
def search(zipcode,imdb,metacrit):
	movies_filt = Findmovies_main(zipcode, imdb, metacrit)
	for each in movies_filt:
		each.createLink(zipcode)

	return render_template('search.html', movies=movies_filt)

if __name__ == '__main__':
	app.run(debug=True)
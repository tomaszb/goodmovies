from flask import Flask, render_template
from findgoodmovies import *

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello world!"

@app.route('/search/<int:zipcode>/<float:imdb>/<int:metacrit>')
def search(zipcode,imdb,metacrit):
	movies_filt = Findmovies_main(zipcode, imdb, metacrit)
	for each in movies_filt:
		each.printMovie()

	return render_template('search.html', movies=movies_filt)

if __name__ == '__main__':
	app.run(debug=True)
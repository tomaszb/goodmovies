from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flaskext.lesscss import lesscss
from findgoodmovies import *

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
	error = None
	print "got here"
	imdb_value = request.args.get("imdb-value")
	metacritic_value = request.args.get("metacritic-value")
	zipcode_value = request.args.get("zipcode-input")
	if imdb_value != None and metacritic_value != None and zipcode_value != None:
		print "here now"
		imdb = float(imdb_value)/10.0
		metacrit = float(metacritic_value)
		zipcode = zipcode_value
		movies_filt = Findmovies_main(zipcode, imdb, metacrit)
		for each in movies_filt:
			each.createLink(zipcode)

		return render_template('search.html', movies=movies_filt)

	else:
		return "Error!"

if __name__ == '__main__':
	app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from findgoodmovies import *

app = Flask(__name__)
Bootstrap(app)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
	error = None

	imdb_value = request.args.get("imdb-value")
	metacritic_value = request.args.get("metacritic-value")
	zipcode_value = request.args.get("zipcode-input")

	
	if imdb_value != None and metacritic_value != None and zipcode_value != None:
		imdb = float(imdb_value)/10.0
		metacrit = float(metacritic_value)
		zipcode = zipcode_value
		movies_filt = Findmovies_main(zipcode, imdb, metacrit)
		print "what about here"
		for each in movies_filt:
			each.createLink(zipcode)

		return_json = request.args.get('json')

		if return_json != None and return_json == "true":
			testing = dictifyMovies(movies_filt)
			print "is it here"
			print testing
			return jsonify(dictifyMovies(movies_filt))
		else:
			return render_template('search.html', movies=movies_filt)

	else:
		return "Error!"

if __name__ == '__main__':
	app.run(host='0.0.0.0')
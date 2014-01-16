from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
import re
import dbManager

class MovieSearch:
	def __init__(self):
		self.movies = []

	def addTimeToMovieOrCreate(self, title, theater, times, imdb_url):
		#adds movie times to movie and first creates movie if it doesn't exist
		movie_item = [item for item in self.movies if item.title == title]
		if len(movie_item) > 0:
			movie_item[0].addTimes(theater, times)
		else:
			self.movies.append(Movie(title, {theater : times}, imdb_url))

	def getRatings(self):
		db = dbManager.dbMan()
		db.dbConnect()
		for each in self.movies:
			dbMovie = db.returnMovie(each.title)
			if dbMovie != None:
				each.imdb_rating = float(dbMovie.imdbrating/10.0)
				each.metacritic_rating = dbMovie.metacritic
			else:
				each.getIMDBRating()
				db.saveMovie(each.title, each.imdb_rating, each.metacritic_rating)

		db.dbDC()


	def printAll(self):
		#prints all data for each movie
		for each in self.movies:
			each.printMovie()

class Movie:
	def __init__(self, title, times = {}, imdb_url = ""):
		self.title = title
		self.times = times
		self.imdb_url = imdb_url
		self.imdb_rating = 0.0
		self.metacritic_rating = 0.0
		self.googLink = u""

	def createLink(self, zipcode):
		self.googLink = u"http://www.google.com/movies?near={0}&q={1}".format(zipcode, self.title.replace(" ","+")) 

	def addTimes(self, theater,times):
		self.times[theater] = times

	def setRatings(self, imdb_rating = 0.0, metacritic_rating = 0.0):
		self.imdb_rating = float(imdb_rating)
		self.metacritic_rating = float(metacritic_rating)

	def getIMDBRating(self):
		#get imdb (and metacritic) rating from imdb html
		if self.imdb_url != None:

			print "Getting Ratings for %s" % self.title
			soup = bs(urlopen(self.imdb_url))
			try:
				imdb_rating = soup.find('div', 'star-box-giga-star').text.strip()
			except:
				imdb_rating = u'0'
			
			regex = re.compile("Metascore:\s\s\d\d\d?")
			try:
				metacritic_rating = regex.findall(soup.find('div','star-box-details').text)[0].split(":")[1].strip()
			except:
				metacritic_rating = u'0'

			self.setRatings(imdb_rating,metacritic_rating)

		else:
			self.setRatings(u'0',u'0')

	def printMovie(self):
		print "Title: " +  self.title
		for key, value in self.times.iteritems():
			print "  Theater: " + key
			print "  Times: " + " ".join(value)
		print "  IMDB Rating: " + str(self.imdb_rating)
		print "  Metacritic Rating: " + str(self.metacritic_rating)
		print '\n\n'

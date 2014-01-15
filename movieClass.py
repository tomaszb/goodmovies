from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
import re

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

	def addTimes(self, theater,times):
		self.times[theater] = times

	def setRatings(self, imdb_rating = 0.0, metacritic_rating = 0.0):
		self.imdb_rating = int(float(imdb_rating)*10)
		self.metacritic_rating = float(metacritic_rating)

	def getIMDBRating(self):
		#get imdb (and metacritic) rating from imdb html
		print "Getting Ratings for %s" % self.title
		soup = bs(urlopen(self.imdb_url))
		imdb_rating = soup.find('div', 'star-box-giga-star').text.strip()
		
		regex = re.compile("Metascore:\s\s\d\d\d?")
		try:
			metacritic_rating = regex.findall(soup.find('div','star-box-details').text)[0].split(":")[1].strip()
		except:
			metacritic_rating = u'0'

		self.setRatings(imdb_rating,metacritic_rating)

	def printMovie(self):
		print "Title: " +  self.title
		for key, value in self.times.iteritems():
			print "  Theater: " + key
			print "  Times: " + " ".join(value)
		print "  IMDB Rating: " + str(self.imdb_rating)
		print "  Metacritic Rating: " + str(self.metacritic_rating)
		print '\n\n'

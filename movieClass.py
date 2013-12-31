class MovieSearch:
	def __init__(self):
		self.movies = []

	def addTimeToMovieOrCreate(self, title, theater, times):
		movie_item = [item for item in self.movies if item.title == title]
		if len(movie_item) > 0:
			movie_item[0].addTimes(theater, times)
		else:
			self.movies.append(Movie(title, {theater : times}))

	def printAll(self):
		for each in self.movies:
			print "Title: " +  each.title
			for key, value in each.times.iteritems():
				print "  Theater: " + key
				print "  Times: " + " ".join(value)
			print "  IMDB Rating: " + str(each.imdb_rating)

class Movie:
	def __init__(self, title, times = {}, imdb_rating = 0):
		self.title = title
		self.times = times
		self.imdb_rating = imdb_rating

	def addTimes(self, theater,times):
		self.times[theater] = times

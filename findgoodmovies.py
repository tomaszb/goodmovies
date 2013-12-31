from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys
import re

from movieClass import Movie, MovieSearch


def findMovies(zipcode):
	#finds all movies in zipcode
	if not checkZipCode(zipcode):
		print "Invalid zipcode"
		return None

	movie_coll = getAllMoviesInArea(zipcode)
	if movie_coll == None:
		print "No movies found"
		return None
	else:
		movie_coll.printAll()
		return movie_coll

def getAllMoviesInArea(zipcode):
	soup_pages = []
	base_url = "http://www.google.com/movies?near={0}".format(zipcode)
	
	soup = bs(urlopen(base_url))
	start_int = 10
	while (soup.get_text().find("No showtimes") == -1):
		print start_int
		soup_pages.append(soup)
		url = base_url + "&start={0}".format(start_int)
		print url
		soup = bs(urlopen(url))
		start_int += 10

	if len(soup_pages) == 0:
		return None
	else:
		return parsePages(soup_pages)

def checkZipCode(zipcode):
	#checks if zipcode valid
	return True

def parsePages(pages):
	#parses google movie search results pages
	movie_search = MovieSearch()
	
	for page in pages:
		theaters = page.findAll("div", "theater")
		
		for theater in theaters:
			theater_name = theater.find('h2','name').text
			theater_movies = theater.findAll('div','movie')
			
			for movie in theater_movies:
				movie_name = movie.find('div','name').text
				times = extractMovieTimes(movie.find('div','times').text)

				movie_search.addTimeToMovieOrCreate(movie_name, theater_name, times)

	return movie_search


def extractMovieTimes(times_text):
	#makes list of movie times from google movie results strings
	regex = re.compile("(([1-9]|1[0-2]):([0-5][0-9])(am|pm)?)",re.UNICODE)
	times_list = regex.findall(times_text)
	return [first_time[0] for first_time in times_list]


def processMovieTitle(movie):
	#to be used later
	return '+'.join(movie.split(' '))

if __name__ == "__main__":
	if (len(sys.argv) != 2):
		print "Usage: python mainscript.py <zipcode>"
	else:
		zipcode = sys.argv[1]
		movie_coll = findMovies(zipcode)

		if movie_coll != None:
			findIMDBRatings(movie_coll)
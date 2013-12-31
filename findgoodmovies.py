from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

from movieClass import Movie

def processMovieTitle(movie):
	return '+'.join(movie.split(' '))

def checkZipCode(zipcode):
	#to be filled with regex
	return True

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
		return soup_pages
	else:
		parsePages(soup_pages)

	return soup_pages

def parsePages(pages):
	listofmovies = []
	for page in pages:
		theaters = page.findAll("div", "theater")
		for theater in theaters:
			theater_name = theater.find('h2','name').text
			theater_movies = theater.findAll('div','movie')
			for movie in theater_movies:
				movie_name = movie.find('div','name').text
				
				if contains(listofmovies, lambda x: x.title == movie_name):
					#add times to movie
				else:
					#create new movie
					new_movie = Movie(movie_name)



def conatins(list, filter):
	#to check if movie already exists in list
	for x in list:
		if filter(x):
			return True

	return False

def findGoodMovies(zipcode):
	if not checkZipCode(zipcode):
		return False
	else:
		getAllMoviesInArea(zipcode)

if __name__ == "__main__":
	if (len(sys.argv) != 2):
		print "Usage: python mainscript.py <zipcode>"
	else:
		findGoodMovies(zipcode)
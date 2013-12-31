from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

from movieClass import *

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

	parsePages(soup_pages)

	return soup_pages


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
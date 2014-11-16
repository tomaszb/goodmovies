from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys
import re

from movieClass import Movie, MovieSearch
import time
import json


def findMovies(zipcode):
	#finds all movies in zipcode
	if not checkZipCode(zipcode):
		print "Invalid zipcode"
		return None

	movie_coll = getAllMoviesInArea_Gracenote(zipcode)
	if movie_coll == None:
		print "No movies found"
		return None
	else:
		movie_coll.printAll()
		return movie_coll

def getAllMoviesInArea_Gracenote(zipcode):
	movie_search = MovieSearch()
	base_url = "http://data.tmsapi.com/v1/movies/showings?startDate={0}&zip={1}&api_key=nc2exze38pxshn2z7xw8z5k5".format(time.strftime("%Y-%m-%d"), zipcode)
	resp = urlopen(base_url)
	fulljson = json.loads(resp.read())
	print fulljson
	print "full shit here"

	for movie in fulljson:
		movie_name = movie['title']
		times_dict = {}

		for times in movie['showtimes']:
			
			if not (times['theatre']['name'] in times_dict):
				times_dict[times['theatre']['name']] = []
			
			times_dict[times['theatre']['name']].append(times['dateTime'].split('T')[1])

		for theater_name,times in times_dict.items():
			movie_search.addTimeToMovieOrCreate(movie_name, theater_name, times, movie_name.replace(' ', '+'))
			print "movie_name: " + movie_name + "thether_name: " + theater_name, "times: " + "movie_name: " + movie_name

	return movie_search

def getAllMoviesInArea(zipcode):
	soup_pages = []
	base_url = "http://www.google.com/movies?near={0}".format(zipcode)
	soup = bs(urlopen(base_url))
	start_int = 10
	return soup.get_text()
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

				links_list = movie.findAll('a','fl')
				movie_imdb_url = extractIMDBUrl(links_list)

				movie_search.addTimeToMovieOrCreate(movie_name, theater_name, times, movie_imdb_url)

	return movie_search


def extractMovieTimes(times_text):
	#makes list of movie times from google movie results strings
	regex = re.compile("(([1-9]|1[0-2]):([0-5][0-9])(am|pm)?)",re.UNICODE)
	times_list = regex.findall(times_text)
	return [first_time[0] for first_time in times_list]

def extractIMDBUrl(links_list):
	#finds url for imdb for a specific movie
	whole_a = [x for x in links_list if "IMDb" in x.text]
	if (len(whole_a) == 0):
		return None
	else:
		regex = re.compile("http://www.imdb.com/title/tt\d+")
		print str(whole_a[0])
		imdb_link = regex.findall(str(whole_a[0]))
		if len(imdb_link) > 0:
			return imdb_link[0]
		else:
			return None


def findRatings(movie_coll):
	#to get movie ratings for each movie from each source (first IMDB)
	print "started ratings"
	movie_coll.getRatings()
	print "ended ratings"

def dictifyMovies(movie_list):
	movie_dict = {}
	
	for each in movie_list:
		movie_dict[each.title] = each.dictifyMovie()

	return movie_dict

def printFilteredResults(movie_coll, lowest_imdb, lowest_metacritic):
	imdb = float(lowest_imdb)
	metacritic = float(lowest_metacritic)
	for each in movie_coll.movies:
		each.printMovie()
		print "unfiltered here"
		if (each.imdb_rating > imdb and each.metacritic_rating > metacritic):
			each.printMovie()

def returnFilteredResults(movie_coll, lowest_imdb, lowest_metacritic):
	imdb = float(lowest_imdb)
	metacritic = float(lowest_metacritic)
	filtered_results = []
	for each in movie_coll.movies:
		if (each.imdb_rating > imdb and each.metacritic_rating > metacritic):
			filtered_results.append(each)

	return filtered_results


def processMovieTitle(movie):
	#to be used later
	return '+'.join(movie.split(' '))

def Findmovies_main(zipcode,imdbrating, metacritic):
	movie_coll = findMovies(zipcode)
	if movie_coll != None:
		findRatings(movie_coll)
		return returnFilteredResults(movie_coll, imdbrating, metacritic)

if __name__ == "__main__":
	if (len(sys.argv) != 4):
		print "Usage: python mainscript.py <zipcode> <imdb rating> <metacritic_rating>"
	else:
		zipcode = sys.argv[1]
		movie_coll = findMovies(zipcode)

		if movie_coll != None:
			findRatings(movie_coll)
			printFilteredResults(movie_coll, sys.argv[2], sys.argv[3])

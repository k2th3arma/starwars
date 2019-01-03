import time
from functools import reduce

import requests
import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render


def character(request, name):
	"""
	The character view will take in the name of a character and search swapi for the character information.
	The data is parsed to find other url requests such as: homeworld, movies, ships, vehicles and species.
	Context data is then sent to the html page for display of the parsed data.
	:param request: The page request
	:param name: The name of the character
	:return: Contextualized character data to include sub url data sent to the html page for display
	"""
	url = 'https://swapi.co/api/people/'
	person = requests.get(url, params={'search': name}).json()['results']
	key_pair = {}
	for key, value in person[0].items():
		# Creates a dictionary for the information, while looking for url data
		key_pair[key.replace('_', ' ').capitalize()] = [data['name'] if 'name' in data else (data['title'] if 'title' in data else '')
		                                            for data in (requests.get(url).json() for url in value)] \
													if type(value) is list else value if value.__contains__('http') \
													else value
		# edge case: Home world is not a list url
		if key.__contains__('home'):
			key_pair[key.replace('_', ' ').capitalize()] = requests.get(value).json()['name']
	context = {
		'dict': key_pair,
		'characters': person
	}

	return render(request, 'data/character.html', context)


def characters(request):
	"""
	The characters view is paginated and can be sorted where the cap is 50 characters and the page count is 10 per.
	The sorting and page number is determined by url parameters and will present data to the user according the values
	passed back to the view.
	:param request: The page request
	:parameter ?sort=: This values determines whether the data will be sorted and how it will be sorted
	:parameter ?page=: This value determines which page is to be presented to the user; pages are 10 character per
	:return: Contextualized data sent to the html page for display
	"""
	sort = None
	if request.GET.get('sort') != 'None':
		sort = request.GET.get('sort')
	if sort is None:
		# Gets an unsorted list of characters
		people = list(get_people().values())
		paginator = Paginator(people, 10)
	elif sort is not None:
		# Gets a sorted list of characters based on the parameter sort
		people = [k for k in sort_by_att(get_people(), att=sort)]
		paginator = Paginator(people, 10)

	page = request.GET.get('page')
	people = paginator.get_page(page)
	context = {
		'characters': people,
		'sort': sort
	}
	return render(request, 'data/characters.html', context)


def sort_by_att(data, att):
	"""
	The sort_by_att function takes in the data and the sort parameter and returns the sorted values.
	:param data: The character data
	:param att: The sorting parameter; ascending and descending capable ('-'): descending
	:return: A lists of dictionaries where each dictionary contains the data points for each character
	"""
	if att.__contains__('-'):
		return [data[k] for k in sorted(data, key=lambda x: (data[x][att[1:]]), reverse=True)]
	else:
		return [data[k] for k in sorted(data, key=lambda x: (data[x][att]))]


def get_people():
	"""
	The get_people function will recursively grab characters and their respective data points.
	The functions limit is set to 50 unique characters.

	The dictionary is a	dictionary of dictionaries where the main key is the order of reading and
	the nested dictionary is the character attributes as keys and their respective values.
	This function also normalizes some of the data points on reading, this allows for more optimal
	sorting.

	:return: Returns a dictionary of characters and their respective data points.
	"""
	url = 'https://swapi.co/api/people/'
	people = requests.get(url).json()
	re = {'unknown': "-1", ',': ''}
	data = {}
	count = 0
	while people['next'] and count < 50:
		for person in people['results']:
			if count < 50:
				data[count] = {'name': person['name'],
				                      'mass': float(reduce(lambda a, kv: a.replace(*kv), re.items(), person['mass'])),
				                      'height': float(reduce(lambda a, kv: a.replace(*kv), re.items(), person['height']))}
				count = count + 1
		people = requests.get(people['next']).json()
	return data


def planet_residents(request):
	"""
	The planet_residents view will recursively find all planets and create a dictionary where the key
	is the planet and name and the value is a list of the residents.
	:param request: The page request
	:return: A JSON file of the all the planets and their respective residents.
	"""
	url = 'https://swapi.co/api/planets/'
	planets = requests.get(url).json()
	json_string = {}
	while planets['next']:
		for planet in planets['results']:
			json_string[planet['name']] = [requests.get(person).json()['name'] for person in planet['residents']]
		planets = requests.get(planets['next']).json()
	dump = json.dumps(json_string, sort_keys=True, indent=4, separators=(',', ':'))
	return HttpResponse(dump, content_type='application/json')

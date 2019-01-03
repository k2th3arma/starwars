from django.urls import path

from . import views

urlpatterns =[
	# Character Page
	path('characters', views.characters, name='characters'),
	# Character Details Page
	path('character/<name>', views.character, name='character'),
	# Planet Resident Page
	path('planet-residents', views.planet_residents, name='planet-residents'),
]
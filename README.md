# Starwars

A simple Star Wars web application that utilizes the Swapi(Star Wars API) database. The application was built using pythons django 
library.
<li>https://swapi.co/</li>

## Views
The web application has three views that pull data from swapi.
### /Character/<String:name>
The character view will take in the name of a character and search swapi for the character information.
	The data is parsed to find other url requests such as: homeworld, movies, ships, vehicles and species.
	Context data is then sent to the html page for display of the parsed data.

### /Characters
The characters view is paginated and can be sorted where the cap is 50 characters and the page count is 10 per.
	The sorting and page number is determined by url parameters and will present data to the user according the values
	passed back to the view.
  
### /planet-residents
The planet_residents view will recursively find all planets and create a dictionary where the key
	is the planet name and the value is a list of the residents. Once all the planets and
	residents have been collected the view will return a JSON file.
  
## Running the Application
I currently run this on Ubuntu 16.04 LTS, so the following instructions will be linux based.

The following is the dependency list to run the applicaiton.
<li>https://github.com/k2th3arma/starwars/blob/master/req.txt</li>


1. Download Repo:
    1. git clone https://github.com/k2th3arma/starwars
    
Once the files have been cloned, there are a couple options to run the application that revolve around the dependencies. 

### Option 1:
If you don't mind having the extra packages run the following:

  pip install -r req.txt ~ This may require sudo and/or -user flag
  
### Option 2
Run the appliction using a virtual environment
  1. Install virtualenv
      1. sudo apt-get install virtualenv
  1. Create the virtual environment 
      1. virtualenv --python=python3 venv
  1. Start the virtual enviroment
      1. source venv/bin/activate
  1. Install the dependencies
      1. pip install -r starwars/req.txt 

### Running the Server
The following command will run the server on port 8000:
  
  1. python starwars/manage.py runserver 0:8000

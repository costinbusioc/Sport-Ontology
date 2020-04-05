from datetime import date
import requests
from bs4 import BeautifulSoup

import re
import csv
import sys
import json
import os
import glob
import pandas as pd

sys.path.append('../../../helpers')
from helpers import write_csv

root_url = "https://www.stadiumguide.com/present/"

team_names = []
capacities = []
stadiums = []
cities = []
countries = []

country_list = ["austria", "belgium", "croatia", "czech-republic", "denmark",
	"england", "france", "germany", "greece", "hungary", "italy", "israel",
	"netherlands", "norway", "poland", "portugal", "romania", "russia",
	"scotland", "serbia", "spain", "sweden", "switzerland", "turkey",
	"ukraine", "wales", "other-european-football-stadiums"]

for country in country_list:
	current_url = root_url + country + "/"
	page = requests.get(current_url)
	soup = BeautifulSoup(page.content, "lxml")

	table_teams = soup.find('table', class_='tablepress').find('tbody')
	classes_table = [""]
	for line in table_teams.find_all('tr'):
		try:
			city = line.find('td', class_='column-1').text.strip()
			club = line.find('td', class_='column-2').text.strip()
			stadium = line.find('td', class_='column-3').find('a').text.strip()
			capacity = line.find('td', class_='column-4').text.strip()
		except:
			continue
		
		team_names.append(club)
		if (country == 'other-european-football-stadiums'):
			countries.append('--')
		else:
			countries.append(country[0].upper() + country[1:])
		cities.append(city)
		stadiums.append(stadium)
		capacities.append(capacity)

cols_name = ['FootballTeam', 'Country', 'City', 'Stadium', 'Capacity']
cols = [team_names, countries, cities, stadiums, capacities]
write_csv('teams_locations.csv', cols_name, cols)



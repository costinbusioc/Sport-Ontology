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
from my_utils import get_country_code, map_code_to_country, get_links, get_season

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

team_names = []
seasons = []
countries = []
championships = []
coaches = []

root_url = 'https://www.transfermarkt.com'

def transform_links(links):
	new_links = []
	for link in links:
		tokens = link.split("/")
		new_link = root_url + "/" + tokens[3] + "/" + "erfolge/pokalwettbewerb/" + tokens[6]
		new_links.append(new_link)
	return new_links

links = get_links()
links = transform_links(links)

# links = ['https://www.transfermarkt.com/uefa-champions-league/erfolge/pokalwettbewerb/CL']
links = ['https://www.transfermarkt.com/europa-league/erfolge/pokalwettbewerb/EL']

for link in links:
	print (link)
	page = requests.get(link, headers = headers)
	soup = BeautifulSoup(page.content, "html.parser")
	tag = soup.find('table', class_="items")
	if tag == None:
		continue
	tag = tag.findNext('tbody')
	rows = tag.find_all('tr')

	country_code = get_country_code(link)
	country = map_code_to_country(country_code)

	championship = rows[0].findNext('td').findNext('a').findNext('a').text.strip()
	
	for row in rows[1:]:
		cols = row.find_all('td')
		if len(cols) == 1:
			championship = cols[0].find('img')['title'].strip()
			continue

		season = cols[0].findNext('a').text.strip()
		season = get_season(season)
		seasons.append(season)
		team = cols[2].text.strip()
		team_names.append(team)
		coach = cols[3].text.strip()
		if coach == "":
			coach = "-"
		coaches.append(coach)
		countries.append(country)
		championships.append(championship.replace(" ", "") + "_" + season)

# cols_name = ['ChampionshipWinner', 'Season', 'Championship', 'Country', 'CoachWinner']
# cols = [team_names, seasons, championships, countries, coaches]
# write_csv('championship_winner.csv', cols_name, cols)

cols_name = ['ChampionshipWinner', 'Season', 'Championship', 'CoachWinner']
cols = [team_names, seasons, championships, coaches]
write_csv('championsLeague_winners.csv', cols_name, cols)

# cols_name = ['ChampionshipWinner', 'Season', 'Championship', 'CoachWinner']
# cols = [team_names, seasons, championships, coaches]
# write_csv('europaLeague_winners.csv', cols_name, cols)

	

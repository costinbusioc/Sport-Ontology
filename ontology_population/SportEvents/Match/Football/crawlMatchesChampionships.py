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
from my_utils import get_country_code, map_code_to_country, get_links, get_season, map_code_to_championship_name

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

root_url = 'https://www.transfermarkt.com'

home_teams = []
away_teams = []
home_scores = []
away_scores = []
winners = [] # HomeTeam, AwayTeam, Draw
stages = []
dates = []

date = '-'

def transform_links(links):
	new_links = []
	for link in links:
		tokens = link.split("/")
		new_link = root_url + "/" + tokens[3] + "/" + "gesamtspielplan/wettbewerb/" + tokens[6]
		new_links.append(new_link)
	return new_links

links = get_links()
links = transform_links(links)

for link in links:
	print (link)

	code = link.split('/')[-1]
	championship_name = map_code_to_championship_name(code)

	if championship_name == 'pass':
		continue

	page = requests.get(link, headers = headers)
	soup = BeautifulSoup(page.content, "html.parser")
	tag = soup.find('select', {'name' : 'saison_id'})
	tag = tag.find_all('option')
	years = []
	for elem in tag[1:]:
		season = elem['value'].strip()
		season = str(int(season))
		years.append(season)
	
	if int(years[len(years) - 1]) < 2000:
		years = years[:years.index('2000') + 1]	

	for year in years:
		home_teams = []
		away_teams = []
		home_scores = []
		away_scores = []
		winners = [] # HomeTeam, AwayTeam, Draw
		stages = []
		dates = []

		championship_link = link + "/saison_id/" + year
		print (championship_link)

		championship_page = requests.get(championship_link, headers = headers)
		championship_soup = BeautifulSoup(championship_page.content, "html.parser")
		championship_tag = championship_soup.find_all('div', class_ = "large-6 columns")

		for elem in championship_tag:
			if elem.find('div') != None and elem.find('div').find('div') != None and \
				'Matchday' in elem.find('div').find('div').text:
				stage = elem.find('div').find('div').text.strip()
				print (stage)
				rows = elem.find('tbody').find_all('tr')
			
				for row in rows:
					try:
						class_name = row['class'][0]
					except:
						class_name = ''
					if class_name == 'bg_blau_20':
						try:
							pos_date = row.find('a').text.strip()
							if pos_date != "":
								date = pos_date
						except:
							date = date
					else:
						cols = row.find_all('td')

						tokens = cols[4].find('a').text.strip().split(":")
						if tokens[0] == '-' or len(tokens) == 1:
							continue

						home_teams.append(cols[3].find('img')['alt'].strip())
						away_teams.append(cols[5].find('img')['alt'].strip())
						home_scores.append(tokens[0])
						if 'AET' in tokens[1]:
							tokens[1] = tokens[1][:tokens[1].index('AET') - 1]
						away_scores.append(tokens[1])
						if int(tokens[0]) > int(tokens[1]):
							winners.append("HomeTeam")
						elif int(tokens[0]) < int(tokens[1]):
							winners.append("AwayTeam")
						else:
							winners.append("Draw")
						dates.append(date)
						stages.append(stage)

		filename = "Campionate/" + championship_name + "_" + year + "!" + str(int(year) + 1) + '.csv'
		cols_name = ['HomeTeam', 'AwayTeam', 'HomeScore',
					 'AwayScore', 'Winner', 'Stage',  "Date"]
		cols = [home_teams, away_teams, home_scores, away_scores, winners, stages, dates]
		write_csv(filename, cols_name, cols)
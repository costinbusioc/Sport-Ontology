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

links = ['https://www.transfermarkt.com/uefa-champions-league/gesamtspielplan/pokalwettbewerb/CL/saison_id/']
links = ['https://www.transfermarkt.com/europa-league/gesamtspielplan/pokalwettbewerb/EL/saison_id/']
links = ['https://www.transfermarkt.com/uefa-cup/gesamtspielplan/pokalwettbewerb/UEFA/saison_id/']
years = [i for i in range(2004, 2009)]
years = [str(year) for year in years]
championship_name = "UEFAChampionsLeague_"
championship_name = "EuropaLeague_"
championship_name = "UEFA-Cup_"

print (years)

for link in links:
	print (link)
	for year in years:
		print (year)

		home_teams = []
		away_teams = []
		home_scores = []
		away_scores = []
		winners = [] # HomeTeam, AwayTeam, Draw
		stages = []
		stage_winners = []
		dates = []

		season_link = link + year
		page = requests.get(season_link, headers = headers)
		soup = BeautifulSoup(page.content, "html.parser")

		groups_list = soup.find_all('div', class_ = 'table-header')
		groups_list = groups_list[1:]
		for group in groups_list:
			stage = group.text.strip()
			if stage == 'Knockout stage':
				continue
			print (stage)

			matches = group.findNext('table').findNext('table').find('tbody')
			rows = matches.find_all('tr')
			rows = rows[1:]
			for row in rows:
				try:
					class_name = row['class'][0]
				except:
					class_name = ''
				if class_name == 'bg_blau_20':
					try:
						pos_date = row.find('a').text.strip()
						if pos_date != '':
							date = pos_date
					except:
						date = date
				else:
					cols = row.find_all('td')

					tokens = cols[3].find('a').text.strip().split(":")

					home_teams.append(cols[2].find('img')['alt'].strip())
					away_teams.append(cols[4].find('img')['alt'].strip())
					home_scores.append(tokens[0])
					away_scores.append(tokens[1])
					if int(tokens[0]) > int(tokens[1]):
						winners.append("HomeTeam")
					elif int(tokens[0]) < int(tokens[1]):
						winners.append("AwayTeam")
					else:
						winners.append("Draw")
					dates.append(date)
					stages.append(stage)
					stage_winners.append('-')

					# print (home_teams[-1], " ", home_scores[-1], "-",
					# 	   away_scores[-1], " ", away_teams[-1])

		knockout = soup.find('div', class_ = 'table-header')
		knockout_rounds = knockout.findNext('table').find_all('tbody')
		for i in range(len(knockout_rounds) - 1, -1, -1):
			rows = knockout_rounds[i].find_all('tr')
			stage = rows[0].find('a').text.strip()
			print (stage)

			for row in rows[1:]:
				try:
					class_name = row['class'][0]
				except:
					class_name = ''
				if class_name == 'bg_blau_20':
					try:
						pos_date = row.find('a').text.strip()
						if pos_date != '':
							date = pos_date
					except:
						date = date
				else:
					cols = row.find_all('td')

					tokens = cols[4].find('a').text.strip().split(":")
					tokens[1] = tokens[1].split(' ')[0]

					home_team = cols[3].find('img')['alt'].strip()
					away_team = cols[5].find('img')['alt'].strip()
					home_teams.append(home_team)
					away_teams.append(away_team)
					home_scores.append(tokens[0])
					away_scores.append(tokens[1])
					if int(tokens[0]) > int(tokens[1]):
						winners.append("HomeTeam")
					elif int(tokens[0]) < int(tokens[1]):
						winners.append("AwayTeam")
					else:
						winners.append("Draw")
					dates.append(date)
					stages.append(stage)

					if 'bg_gelb_20' in cols[3]['class']:
						stage_winner = home_team
					elif 'bg_gelb_20' in cols[5]['class']:
						stage_winner = away_team
					else:
						stage_winner = '-'
					stage_winners.append(stage_winner)

					# print (home_teams[-1], " ", home_scores[-1], "-",
					# 	   away_scores[-1], " ", away_teams[-1])


		filename = "Campionate/" + championship_name + year + "!" + str(int(year) + 1) + '.csv'
		cols_name = ['HomeTeam', 'AwayTeam', 'HomeScore',
					 'AwayScore', 'Winner', 'Stage',  'StageWinner', 'Date']
		cols = [home_teams, away_teams, home_scores, away_scores,
				winners, stages, stage_winners, dates]
		write_csv(filename, cols_name, cols)


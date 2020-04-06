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

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

team_names = []
countries = []
squads_no = []
avg_ages = []
no_foreigners = []
players_total_values = []
coaches = []
age_coaches = []

player_names = []
player_tshirt_numbers = []
player_team_names = []
player_ages = []
player_birth_dates = []
player_nationalities = []
player_values = []
players_positions = []

root_url = 'https://www.transfermarkt.com'

links = ['https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/A1',
		 'https://www.transfermarkt.com/2-liga/startseite/wettbewerb/A2',
		 'https://www.transfermarkt.com/premyer-liqasi/startseite/wettbewerb/AZ1',
		 'https://www.transfermarkt.com/primera-divisio/startseite/wettbewerb/AND1',
		 'https://www.transfermarkt.com/kategoria-superiore/startseite/wettbewerb/ALB1',
		 'https://www.transfermarkt.com/bardsragujn-chumb/startseite/wettbewerb/ARM1',
		 'https://www.transfermarkt.com/vysheyshaya-liga/startseite/wettbewerb/WER1',
		 'https://www.transfermarkt.com/pershaja-liga/startseite/wettbewerb/WER2',
		 'https://www.transfermarkt.com/jupiler-pro-league/startseite/wettbewerb/BE1',
		 'https://www.transfermarkt.com/proximus-league/startseite/wettbewerb/BE2',
		 'https://www.transfermarkt.com/premijer-liga/startseite/wettbewerb/BOS1',
		 'https://www.transfermarkt.com/efbet-liga/startseite/wettbewerb/BU1',
		 'https://www.transfermarkt.com/vtora-liga/startseite/wettbewerb/BU2',
		 'https://www.transfermarkt.com/1-hnl/startseite/wettbewerb/KR1',
		 'https://www.transfermarkt.com/2-hnl/startseite/wettbewerb/KR2',
		 'https://www.transfermarkt.com/first-division/startseite/wettbewerb/ZYP1',
		 'https://www.transfermarkt.com/fortuna-liga/startseite/wettbewerb/TS1',
		 'https://www.transfermarkt.com/fortuna-narodni-liga/startseite/wettbewerb/TS2',
		 'https://www.transfermarkt.com/superligaen/startseite/wettbewerb/DK1',
		 'https://www.transfermarkt.com/nordicbet-liga/startseite/wettbewerb/DK2',
		 'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1',
		 'https://www.transfermarkt.com/championship/startseite/wettbewerb/GB2',
		 'https://www.transfermarkt.com/league-one/startseite/wettbewerb/GB3',
		 'https://www.transfermarkt.com/veikkausliiga/startseite/wettbewerb/FI1',
		 'https://www.transfermarkt.com/ykkonen/startseite/wettbewerb/FI2',
		 'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1',
		 'https://www.transfermarkt.com/ligue-2/startseite/wettbewerb/FR2',
		 'https://www.transfermarkt.com/crystalbet-erovnuli-liga/startseite/wettbewerb/GE1N',
		 'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1',
		 'https://www.transfermarkt.com/2-bundesliga/startseite/wettbewerb/L2',
		 'https://www.transfermarkt.com/3-liga/startseite/wettbewerb/L3',
		 'https://www.transfermarkt.com/super-league-1/startseite/wettbewerb/GR1',
		 'https://www.transfermarkt.com/super-league-2/startseite/wettbewerb/GRS2',
		 'https://www.transfermarkt.com/nemzeti-bajnoksag/startseite/wettbewerb/UNG1',
		 'https://www.transfermarkt.com/pepsi-max-deild/startseite/wettbewerb/IS1',
		 'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1',
		 'https://www.transfermarkt.com/serie-b/startseite/wettbewerb/IT2',
		 'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/KAS1',
		 'https://www.transfermarkt.com/divizia-nationala/startseite/wettbewerb/MO1N',
		 'https://www.transfermarkt.com/eredivisie/startseite/wettbewerb/NL1',
		 'https://www.transfermarkt.com/keuken-kampioen-divisie/startseite/wettbewerb/NL2',
		 'https://www.transfermarkt.com/eliteserien/startseite/wettbewerb/NO1',
		 'https://www.transfermarkt.com/pko-ekstraklasa/startseite/wettbewerb/PL1',
		 'https://www.transfermarkt.com/liga-nos/startseite/wettbewerb/PO1',
		 'https://www.transfermarkt.com/liga-pro/startseite/wettbewerb/PO2',
		 'https://www.transfermarkt.com/liga-1/startseite/wettbewerb/RO1',
		 'https://www.transfermarkt.com/liga-2/startseite/wettbewerb/RO2',
		 'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/RU1',
		 'https://www.transfermarkt.com/1-division/startseite/wettbewerb/RU2',
		 'https://www.transfermarkt.com/scottish-premiership/startseite/wettbewerb/SC1',
		 'https://www.transfermarkt.com/super-liga-srbije/startseite/wettbewerb/SER1',
		 'https://www.transfermarkt.com/prva-liga-srbije/startseite/wettbewerb/SER2',
		 'https://www.transfermarkt.com/fortuna-liga/startseite/wettbewerb/SLO1',
		 'https://www.transfermarkt.com/prva-liga/startseite/wettbewerb/SL1',
		 'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1',
		 'https://www.transfermarkt.com/laliga2/startseite/wettbewerb/ES2',
		 'https://www.transfermarkt.com/allsvenskan/startseite/wettbewerb/SE1',
		 'https://www.transfermarkt.com/superettan/startseite/wettbewerb/SE2',
		 'https://www.transfermarkt.com/super-league/startseite/wettbewerb/C1',
		 'https://www.transfermarkt.com/challenge-league/startseite/wettbewerb/C2',
		 'https://www.transfermarkt.com/super-lig/startseite/wettbewerb/TR1',
		 'https://www.transfermarkt.com/1-lig/startseite/wettbewerb/TR2',
		 'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/UKR1',
		 'https://www.transfermarkt.com/persha-liga/startseite/wettbewerb/UKR2']

# links = ['https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/RU1']

def get_country_code(link):
	tokens = link.split("/")
	if tokens[-1][-1] == 'N' and tokens[-1][-2] == '1':
		code = tokens[-1][:-2]
	else:
		code = tokens[-1][:-1]
	return code

def map_code_to_country(code):
	switcher = {
		'A': 'Austria',
		'AZ': 'Azerbaijan',
		'AND': 'Andorra',
		'ALB': 'Albania',
		'ARM': 'Armenia',
		'WER': 'Belarus',
		'BE': 'Belgium',
		'BOS': 'Bosnia and Herzegovina',
		'BU': 'Bulgaria',
		'KR': 'Croatia',
		'ZYP': 'Cyprus',
		'TS': 'Czech Republic',
		'DK': 'Denmark',
		'GB': 'United Kingdom',
		'FI': 'Finland',
		'FR': 'France',
		'GE': 'Georgia',
		'L': 'Germany',
		'GR': 'Greece',
		'GRS': 'Greece',
		'UNG': 'Hungary',
		'IS': 'Iceland',
		'IT': 'Italy',
		'KAS': 'Kazakhstan',
		'MO': 'Moldova',
		'NL': 'Netherlands',
		'NO': 'Norway',
		'PL': 'Poland',
		'PO': 'Portugal',
		'RO': 'Romania',
		'RU': 'Russia',
		'SC': 'Scotland',
		'SER': 'Serbia',
		'SLO': 'Slovakia',
		'SL': 'Slovenia',
		'ES': 'Spain',
		'SE': 'Sweden',
		'C': 'Switzerland',
		'TR': 'Turkey',
		'UKR': 'Ukraine',
	}
	return switcher[code]

for link in links:
	print (link)
	page = requests.get(link, headers = headers)
	soup = BeautifulSoup(page.content, "html.parser")
	tag = soup.find('table', class_="items")
	tag = tag.findNext('tbody')
	rows = tag.find_all('tr')

	country_code = get_country_code(link)
	country = map_code_to_country(country_code)
	
	for row in rows:
		cols = row.find_all('td')
		if int(cols[3].findNext('a').text.strip()) <= 14:
			continue

		team_name = cols[1].findNext('a').text.strip()
		team_names.append(team_name)
		countries.append(country)
		squads_no.append(cols[3].findNext('a').text.strip())
		avg_ages.append(cols[3].findNext('td').text.strip())
		no_foreigners.append(cols[3].findNext('td').findNext('td').text.strip())
		players_total_values.append(cols[4].findNext('a').text.strip())

		team_link = cols[1].findNext('a')['href']
		team_link = root_url + team_link
		print (team_name)
		
		team_page = requests.get(team_link, headers = headers)
		new_soup = BeautifulSoup(team_page.content, "html.parser")

		new_tag = new_soup.find('b', itemprop = "jobTitle")
		if new_tag != None and new_tag.findPrevious('div') != None and new_tag.findPrevious('div').findPrevious('div') != None:
			coaches.append(new_tag.findPrevious('div').findPrevious('div').text.strip())
			age_coaches.append(new_tag.findNext('b').next_sibling.strip())
		else:
			coaches.append("-")
			age_coaches.append("-")

		new_tag = new_soup.find('table', class_="items")
		if new_tag == None:
			continue
		new_tag = new_tag.findNext('tbody')
		new_rows = new_tag.find_all('tr', {'class':['even', 'odd']})

		for new_row in new_rows:
			new_cols = new_row.find_all('td')
			player_tshirt_numbers.append(new_cols[0].findNext('div').text)
			players_positions.append(new_cols[0]['title'])
			player_names.append(new_cols[5].text.strip())
			player_birth_dates.append(new_cols[6].text.strip().split('(')[0])
			player_ages.append('' + new_cols[6].text.strip().split('(')[1][:-1] + " Years")
			player_team_names.append(team_name)
			player_nationalities.append(new_cols[7].findNext('img')['title'].strip())
			player_values.append(new_cols[8].text.strip())

cols_name = ['TeamName', 'Country', 'NoPlayers', 'AvgAge', 'NoForeigners',
	'TotalPlayersValue', 'Coach', 'AgeCouch']
cols = [team_names, countries, squads_no, avg_ages, no_foreigners,
	players_total_values, coaches, age_coaches]
write_csv('teams.csv', cols_name, cols)

cols_name = ['PlayerName', 'Age', 'Birthdate', 'Nationality',
	'Position', 'Club', 'TShirtNumber', 'Value']
cols = [player_names, player_ages, player_birth_dates, player_nationalities,
	players_positions, player_team_names, player_tshirt_numbers, player_values]
write_csv('players.csv', cols_name, cols)

# print (team_names)
# print (squads_no)
# print (avg_ages)
# print (no_foreigners)
# print (players_total_values)
# print (coaches)
# print (age_coaches)

# print (players_positions)
# print (player_names)
# print (player_birth_dates)
# print (player_ages)
# print (player_nationalities)
# print (player_team_names)
# print (player_tshirt_numbers)
# print (player_values)





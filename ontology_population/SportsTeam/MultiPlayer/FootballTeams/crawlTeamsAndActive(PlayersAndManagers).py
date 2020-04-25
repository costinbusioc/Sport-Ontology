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
countries = []
squads_no = []
avg_ages = []
no_foreigners = []
players_total_values = []
coaches = []
age_coaches = []
stadiums = []
stadiums_capacity = []

player_names = []
player_tshirt_numbers = []
player_team_names = []
player_ages = []
player_birth_dates = []
player_nationalities = []
player_values = []
players_positions = []
captains = []

transfer_player_name = []
transfer_season = []
transfer_join_date = []
transfer_end_date = []
transfer_left_team = []
transfer_joined_team = []
transfer_value_or_type = []

coaches_name = []
coaches_nationality = []
coaches_trained_teams = []
coaches_team_country = []
coaches_from_date = []
coaches_end_date = []
coaches_position = []

root_url = 'https://www.transfermarkt.com'

links = get_links()

# links = ['https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1']

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
			coach_name = new_tag.findPrevious('div').findPrevious('div').text.strip()
			coaches.append(coach_name)
			age_coaches.append(new_tag.findNext('b').next_sibling.strip())

			coach_link = root_url + new_tag.findPrevious('a')['href']
			print (coach_link)
			coach_page = requests.get(coach_link, headers = headers)
			coach_soup = BeautifulSoup(coach_page.content, "html.parser")
			coach_tag = coach_soup.find('table', class_ = 'items')
			if coach_tag != None:
				coach_tag = coach_tag.findNext('tbody')
				coach_rows = coach_tag.find_all('tr')
				for coach_row in coach_rows:				
					coach_cols = coach_row.find_all('td')
					if len(coach_cols) < 4:
						continue
					coaches_name.append(coach_name)
					coaches_nationality.append(coach_soup.find('table', class_ = 'auflistung').findNext('img')['title'].strip())
					coaches_trained_teams.append(coach_cols[0].findNext('img')['alt'].strip())
					if coach_cols[1].find('img') != None:
						coaches_team_country.append(coach_cols[1].find('img')['alt'].strip())
					else:
						coaches_team_country.append(coach_cols[1].find('a').text.strip())
					coaches_from_date.append(coach_cols[2].text.strip())
					coaches_end_date.append(coach_cols[3].text.strip())
					coaches_position.append(coach_cols[4].text.strip())

		else:
			coaches.append("-")
			age_coaches.append("-")

		stadium_tag = new_soup.find_all('span', class_ = 'tabellenplatz')
		if len(stadium_tag) < 2:
			stadiums_capacity.append('-')
			stadiums.append('-')
		else:
			stadiums_capacity.append(stadium_tag[1].text.strip())
			stadiums.append(stadium_tag[1].findPrevious('a').text.strip())




		new_tag = new_soup.find('table', class_="items")
		if new_tag == None:
			continue
		new_tag = new_tag.findNext('tbody')
		new_rows = new_tag.find_all('tr', {'class':['even', 'odd']})

		for new_row in new_rows:
			new_cols = new_row.find_all('td')
			player_tshirt_numbers.append(new_cols[0].findNext('div').text)
			players_positions.append(new_cols[0]['title'])

			try:
				captain = new_cols[3].findNext('div').findNext('div').findNext('span').findNext('span')['title']
				if captain == "Team captain":
					captains.append("Team captain")
				else:
					captains.append("-")
			except:
				captains.append("-")

			player_name = new_cols[5].text.strip()
			player_names.append(player_name)
			player_birth_dates.append(new_cols[6].text.strip().split('(')[0])
			player_ages.append('' + new_cols[6].text.strip().split('(')[1][:-1] + " Years")
			player_team_names.append(team_name)
			player_nationalities.append(new_cols[7].findNext('img')['title'].strip())
			player_values.append(new_cols[8].text.strip())

			# merg mai departe pe profilul jucatorului
			print (player_name)

			player_link = root_url + new_cols[3].findNext('a')['href']
			player_page = requests.get(player_link, headers = headers)
			players_soup = BeautifulSoup(player_page.content, "html.parser")
			transfers = players_soup.find_all('tr', class_ = "zeile-transfer")
			for transfer in transfers:
				player_cols = transfer.find_all('td')

				transfer_player_name.append(player_name)
				transfer_season.append(get_season(player_cols[0].text.strip()))
				transfer_join_date.append(player_cols[1].text.strip())
				transfer_left_team.append(player_cols[2].findNext('img')['alt'].strip())
				transfer_joined_team.append(player_cols[6].findNext('img')['alt'].strip())
				transfer_value_or_type.append(player_cols[11].text.strip())

			for i in range(len(transfers)):
				if i == 0:
					transfer_end_date.append("-")
				else:
					transfer_end_date.append(transfer_join_date[-len(transfers) + i - 1])

			===== pentru verificare =====
			print (player_name)
			for i in range(len(transfers)):
				print (transfer_join_date[-len(transfers) + i], " ", transfer_end_date[-len(transfers) + i])
				print (transfer_season[-len(transfers) + i])
				print (transfer_left_team[-len(transfers) + i])
				print (transfer_joined_team[-len(transfers) + i])
				print (transfer_value_or_type[-len(transfers) + i])


cols_name = ['TeamName', 'Country', 'NoPlayers', 'AvgAge', 'NoForeigners',
	'TotalPlayersValue', 'Coach', 'AgeCouch', 'Stadium', 'StadiumCapacity']
cols = [team_names, countries, squads_no, avg_ages, no_foreigners,
	players_total_values, coaches, age_coaches, stadiums, stadiums_capacity]
write_csv('teams.csv', cols_name, cols)

cols_name = ['ManagerName', 'Nationality', 'WorkedInClub', 'CountryClub', 'FromDate', 'ToDate', 'Position']
cols = [coaches_name, coaches_nationality, coaches_trained_teams,
		coaches_team_country, coaches_from_date,
		coaches_end_date, coaches_position]
write_csv('active_managers_history.csv', cols_name, cols)

cols_name = ['PlayerName', 'Age', 'Birthdate', 'Nationality',
	'Position', 'Club', 'TShirtNumber', 'Value', 'Captain']
cols = [player_names, player_ages, player_birth_dates, player_nationalities,
	players_positions, player_team_names, player_tshirt_numbers,
  player_values, captains]
write_csv('players.csv', cols_name, cols)

cols_name = ['PlayerName', 'Season','JoinDate', 'EndDate',
			 'LeftTeam', 'JoinedTeam', 'Value']
cols = [transfer_player_name, transfer_season, transfer_join_date,
		transfer_end_date, transfer_left_team, transfer_joined_team,
		transfer_value_or_type]
write_csv('players_history.csv', cols_name, cols)




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
from my_utils import get_country_code, map_code_to_country, get_links, get_season, get_list_

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

transfer_player_name = []
transfer_player_nationality = []
transfer_season = []
transfer_join_date = []
transfer_end_date = []
transfer_left_team = []
transfer_left_team_country = []
transfer_joined_team_country = []
transfer_joined_team = []
transfer_value_or_type = []

coaches_name = []
coaches_nationality = []
coaches_trained_teams = []
coaches_team_country = []
coaches_from_date = []
coaches_end_date = []
coaches_position = []

coaches_name_set = set([])
players_name_set = set([])

root_url = 'https://www.transfermarkt.com'
concat_url = '/plus/?saison_id='

loaded_coach_names = list(set(get_list_('active_managers_history.csv', 'ManagerName')))
loaded_player_names = list(set(get_list_('active_players_history.csv', 'PlayerName')))

links = get_links()

# links = ['https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1',
# 		 'https://www.transfermarkt.com/liga-2/startseite/wettbewerb/RO2']

for link in links:
	print (link)
	page = requests.get(link, headers = headers)
	soup = BeautifulSoup(page.content, "html.parser")
	tag = soup.find('select', {'name' : 'saison_id'})
	tag = tag.find_all('option')
	years = []
	for elem in tag:
		season = elem.text.strip()
		if '/' in season:
			season = get_season(season).split('/')[0]
		else:
			season = str(int(season) - 1)
		years.append(season)

	country_code = get_country_code(link)
	country = map_code_to_country(country_code)
	
	if int(years[len(years) - 1]) < 1980:
		years = years[:years.index('1980') + 1]

	if country_code == 'ES':
		years = years[:years.index('1986') + 1]

	print (years)
	
	for year in years:
		year_url = link + concat_url + year
		print (year_url)
		year_page = requests.get(year_url, headers = headers)
		year_soup = BeautifulSoup(year_page.content, "html.parser")

		year_tag = year_soup.find('table', class_="items")
		year_tag = year_tag.findNext('tbody')
		rows = year_tag.find_all('tr')
		
		for row in rows:
			cols = row.find_all('td')
			if int(cols[3].findNext('a').text.strip()) <= 14:
				continue

			team_name = cols[1].findNext('a').text.strip()

			team_link = cols[1].findNext('a')['href']
			team_link = root_url + team_link
			print ("===== Country: ", country, " ===== Year: ",
					year, " ===== Team: ", team_name, " =====")
			
			team_page = requests.get(team_link, headers = headers)
			new_soup = BeautifulSoup(team_page.content, "html.parser")

			new_tag = new_soup.find('div', class_ = 'container-foto')
			if new_tag != None and new_tag.findNext('img') != None:
				coach_name = new_tag.findNext('img')['title'].strip()
				coach_link = root_url + new_tag.findNext('a')['href']
				print ("Coach: ", coach_link)

				# daca nu e deja in lista, adaug detalii pentru antrenor
				if coach_name not in coaches_name_set and coach_name not in loaded_coach_names:
					coaches_name_set.add(coach_name)

					coach_page = requests.get(coach_link, headers = headers)
					coach_soup = BeautifulSoup(coach_page.content, "html.parser")
					coach_tag = coach_soup.find('table', class_ = 'items')
					if coach_tag != None:
						coach_tag = coach_tag.findNext('tbody')
						coach_rows = coach_tag.find_all('tr')
						nation_tag = coach_soup.find('table', class_ = 'auflistung').find('img')
						if nation_tag != None and 'title' in nation_tag:
							coach_nationality = nation_tag['title'].strip()
						else:
							coach_nationality = '-'
						for coach_row in coach_rows:				
							coach_cols = coach_row.find_all('td')
							if len(coach_cols) < 4:
								continue
							coaches_name.append(coach_name)
							coaches_nationality.append(coach_nationality)
							coaches_trained_teams.append(coach_cols[0].findNext('img')['alt'].strip())
							if coach_cols[1].find('img') != None:
								coaches_team_country.append(coach_cols[1].find('img')['alt'].strip())
							else:
								coaches_team_country.append(coach_cols[1].find('a').text.strip())
							coaches_from_date.append(coach_cols[2].text.strip())
							coaches_end_date.append(coach_cols[3].text.strip())
							coaches_position.append(coach_cols[4].text.strip())

			new_tag = new_soup.find('table', class_="items")
			if new_tag == None:
				continue
			new_tag = new_tag.findNext('tbody')
			new_rows = new_tag.find_all('tr', {'class':['even', 'odd']})

			for new_row in new_rows:
				new_cols = new_row.find_all('td')

				player_name = new_cols[3].findNext('a').text.strip()
				print (player_name)
				# merg mai departe pe profilul jucatorului
				if player_name not in players_name_set and player_name not in loaded_player_names:
					players_name_set.add(player_name)

					player_link = root_url + new_cols[3].findNext('a')['href']
					player_page = requests.get(player_link, headers = headers)
					players_soup = BeautifulSoup(player_page.content, "html.parser")

					if ',' in new_cols[5].text.strip():
						player_nationality = new_cols[6].find('img')['title']
					else:
						player_nationality = new_cols[7].find('img')['title']

					transfers = players_soup.find_all('tr', class_ = "zeile-transfer")
					if transfers != None:
						for transfer in transfers:
							player_cols = transfer.find_all('td')

							transfer_player_name.append(player_name)
							transfer_player_nationality.append(player_nationality)
							transfer_season.append(get_season(player_cols[0].text.strip()))
							transfer_join_date.append(player_cols[1].text.strip())
							transfer_left_team.append(player_cols[2].findNext('img')['alt'].strip())

							if player_cols[3].find('img') != None:
								transfer_left_team_country.append(player_cols[3].findNext('img')['title'].strip())
							else:
								transfer_left_team_country.append("-")

							transfer_joined_team.append(player_cols[6].findNext('img')['alt'].strip())

							if player_cols[7].find('img') != None:
								transfer_joined_team_country.append(player_cols[7].findNext('img')['title'].strip())
							else:
								transfer_joined_team_country.append("-")

							transfer_value_or_type.append(player_cols[11].text.strip())

						for i in range(len(transfers)):
							if i == 0:
								transfer_end_date.append("-")
							else:
								transfer_end_date.append(transfer_join_date[-len(transfers) + i - 1])

	cols_name = ['ManagerName', 'Nationality', 'WorkedInClub', 'Country', 'FromDate', 'ToDate', 'Position']
	cols = [coaches_name, coaches_nationality, coaches_trained_teams, coaches_team_country,
			coaches_from_date, coaches_end_date, coaches_position]
	write_csv('2_retired_managers_history.csv', cols_name, cols)

	cols_name = ['PlayerName', 'Nationality', 'Season','JoinDate', 'EndDate',
				 'LeftTeam', 'CountryLeftTeam', 'JoinedTeam', 
				 'CountryJoinedTeam', 'Value']
	cols = [transfer_player_name, transfer_player_nationality, transfer_season,
			transfer_join_date, transfer_end_date, transfer_left_team,
			transfer_left_team_country,	transfer_joined_team,
			transfer_joined_team_country, transfer_value_or_type]
	write_csv('2_retired_players_history.csv', cols_name, cols)
	print ("Am salvat pentru link-ul: ", link)




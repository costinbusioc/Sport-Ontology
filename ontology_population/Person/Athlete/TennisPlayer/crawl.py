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

root_url = "https://www.atptour.com/en/rankings/singles/?rankDate=2020-3-16&countryCode=all&rankRange="

paranthesis = re.compile(r'\([^)]*\)')

players_names = []
players_urls = []
players_age = []
players_rank = []

for nr_page in range(14):
    current_url = f"{root_url}{nr_page * 100 + 1}-{(nr_page + 1) * 100}"
    page = requests.get(current_url)
    soup = BeautifulSoup(page.content, "html.parser")

    players_table = soup.find('table', class_='mega-table')

    for player_row in players_table.find('tbody').find_all('tr'):
        player_name = player_row.find('td', class_='player-cell').find('a').text.strip()
        player_url = player_row.find('td', class_='player-cell').find('a')['href']
        player_age = player_row.find('td', class_='age-cell').text.strip()
        player_rank = player_row.find('td', class_='rank-cell').text.strip()

        players_names.append(player_name)
        players_urls.append(player_url)
        players_age.append(player_age)
        players_rank.append(player_rank)

cols_name = ['Name', 'URL', 'Age', 'Rank']
cols = [players_names, players_urls, players_age, players_rank]
write_csv('tennis_players.csv', cols_name, cols)

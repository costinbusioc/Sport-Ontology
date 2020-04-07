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

root_url = "https://www.atptour.com/en/rankings/singles/?rankDate="

#dates = ['2020-3-16', '2019-03-18', '2018-03-05', '2017-03-06', '2015-03-09', '2016-03-07']
#dates += ['2014-03-03', '2013-03-04', '2012-03-05', '2012-03-13', '2011-03-07', '2010-03-01']
#dates += ['2009-03-09', '2008-03-03', '2007-03-05', '2006-03-06', '2005-03-07']
dates = ['2004-03-01', '2003-03-10', '2003-3-18', '2001-03-12', '2000-03-06']
dates += ['1999-03-15', '1998-03-16', '1997-03-24', '1996-03-11', '1995-03-06']
dates += ['1994-03-07', '1993-03-01', '1992-03-23', '1991-03-04', '1990-03-12']
dates += ['1989-03-06', '1988-03-07', '1987-03-09', '1986-03-03', '1985-03-03']
dates += ['1984-03-05', '1983-03-21', '1982-03-01', '1981-03-02', '1980-03-24']
dates += ['1979-03-05', '1978-03-06', '1977-03-14', '1976-03-01', '1975-03-05']
dates += ['1974-03-02', '1973-08-23']

paranthesis = re.compile(r'\([^)]*\)')

players_names = []
players_urls = []
players_age = []
players_rank = []

already_saved_players = []
df = pd.read_csv('2015_2020_players.csv')
for idx, row in df.iterrows():
    already_saved_players.append(row['Name'])

df = pd.read_csv('2005_2015_new_players.csv')
for idx, row in df.iterrows():
    already_saved_players.append(row['Name'])

for i in range(0, len(dates)):
    print(dates[i])
    for nr_page in range(14):
        current_url = f"{root_url}{dates[i]}&countryCode=all&rankPage={nr_page * 100 + 1}-{(nr_page + 1) * 100}"
        page = requests.get(current_url)
        soup = BeautifulSoup(page.content, "html.parser")

        players_table = soup.find('table', class_='mega-table')

        for player_row in players_table.find('tbody').find_all('tr'):
            player_name = player_row.find('td', class_='player-cell').find('a').text.strip()
            player_url = player_row.find('td', class_='player-cell').find('a')['href']
            player_age = player_row.find('td', class_='age-cell').text.strip()
            player_rank = player_row.find('td', class_='rank-cell').text.strip()

            if player_name in already_saved_players or player_name in players_names:
                continue

            players_names.append(player_name)
            players_urls.append(player_url)
            players_age.append(player_age)
            players_rank.append(player_rank)


    cols_name = ['Name', 'URL', 'Age', 'Rank']
    cols = [players_names, players_urls, players_age, players_rank]
    write_csv('new_tennis_players.csv', cols_name, cols)

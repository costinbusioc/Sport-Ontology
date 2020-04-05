from datetime import datetime, timedelta
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

root_url = "https://www.atptour.com/"
input_tables = ["tennis_tournaments.csv", "new_tennis_tournaments.csv"]

paranthesis = re.compile(r'\([^)]*\)')

home_names = []
away_names = []
home_scores = []
away_scores = []
tournaments = []
years = []
cities = []
countries = []

for input_table in input_tables:
    df = pd.read_csv(input_table)
    for idx, row in df.iterrows():
        year = row['Year']
        tournament = row['Tournament']
        startDate = row['Start Date']
        city = row['City']
        country = row['Country']
        results_url = row['URL']

        if year < 2014:
            continue

        if year == 2014 and tournament == 'Memphis':
            continue

        year, month, day = startDate.split('.')
        startDate = datetime(int(year), int(month), int(day))

        current_url = f"{root_url}{results_url}"
        page = requests.get(current_url)
        soup = BeautifulSoup(page.content, "html.parser")

        print(tournament)
        print(year)

        table = soup.find('table', class_='day-table')
        sections = table.find_all('tbody')
        for i, section in enumerate(sections):
            matches_section = section.find_all('tr')
            for j, match_section in enumerate(matches_section):
                players = match_section.find_all('td', class_='day-table-name')
                try:
                    player1 = players[0].find('a').text.strip()
                except:
                    continue

                try:
                    player2 = players[1].find('a').text.strip()
                except:
                    continue

                try:
                    score = match_section.find('td', class_='day-table-score')
                except:
                    continue
                try:
                    score = score.find('a').text.strip()
                except:
                    continue
                score = score.split('\n')

                homescore = 0
                awayscore = 0
                if len(score) == 2:
                    homescore = 2
                elif len(score) == 3:
                    homescore = 2
                    awayscore = 1
                elif len(score) == 4:
                    homescore = 3
                    awayscore = 1
                elif len(score) == 5:
                    homescore = 3
                    awayscore = 2

                home_names.append(player1)
                away_names.append(player2)
                home_scores.append(homescore)
                away_scores.append(awayscore)
                tournaments.append(tournament)
                years.append(year)
                cities.append(city)
                countries.append(country)

cols_name = ['Home', 'Away', 'Home Score', 'Away Score', 'Tournament', 'Year', 'City', 'Country']
cols = [home_names, away_names, home_scores, away_scores, tournaments, years, cities, countries]
write_csv('tennis_matches.csv', cols_name, cols)


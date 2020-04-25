from datetime import date
import requests
from bs4 import BeautifulSoup

import re
import csv
import sys
import json
import os
import math
import glob
import pandas as pd

sys.path.append('../../../../helpers')
from helpers import write_csv

root_url = "https://www.atptour.com/en/scores/results-archive?"

paranthesis = re.compile(r'\([^)]*\)')

names = []
years = []
cities = []
countries = []
surfaces = []
prizes = []
champions = []
start_dates = []
urls = []

for year in range(1975, 2005):
    print(year)
    current_url = root_url + f'year={year}&tournamentType=atpg'
    page = requests.get(current_url)
    soup = BeautifulSoup(page.content, "lxml")

    tournament_table = soup.find('table', class_='results-archive-table mega-table').find('tbody')
    for tournament in tournament_table.find_all('tr', class_='tourney-result'):
        title = tournament.find('td', class_='title-content')
        name = title.find('span', class_='tourney-title').text.strip()
        location = title.find('span', class_='tourney-location').text

        try:
            city, country = location.split(',')
            city = city.strip()
            country = country.strip()
        except:
            city = location.strip()
            country = 'Empty'

        start_date = title.find('span', class_='tourney-dates').text.strip()

        finance = tournament.find('td', class_='tourney-details fin-commit')
        try:
            prize = finance.find('span', class_='item-value').text.strip()
        except:
            continue

        winners = tournament.find('td', class_='tourney-details action-buttons')

        try:
            champion = winners.find_all('div', class_='tourney-detail-winner')[0].find('a').text.strip()
        except:
            continue

        details = tournament.find_all('td', class_='tourney-details')
        surface = details[1].find('span').text.strip()
        url = details[4].find('a')['href']

        names.append(name)
        cities.append(city)
        countries.append(country)
        start_dates.append(start_date)
        prizes.append(prize)
        champions.append(champion)
        surfaces.append(surface)
        urls.append(url)
        years.append(year)

    cols_name = ['Tournament', 'City', 'Country', 'Start Date', 'Prize', 'Champion', 'Surface', 'URL', 'Year']
    cols = [names, cities, countries, start_dates, prizes, champions, surfaces, urls, years]
    write_csv('1975_2005_tennis_tournaments.csv', cols_name, cols)

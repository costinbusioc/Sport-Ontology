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

sys.path.append('..')
from helpers import write_csv

root_url = "https://www.worldometers.info/geography/alphabetical-list-of-countries/"

page = requests.get(root_url)
soup = BeautifulSoup(page.content, "html.parser")

countries_table = soup.find('table', class_='table table-hover table-condensed')
paranthesis = re.compile(r'\([^)]*\)')

countries = []

for country_row in countries_table.find('tbody').find_all('tr'):
    country_name = country_row.find('td', style='font-weight: bold; font-size:15px').text
    country_name = re.sub(paranthesis, '', country_name).strip()

    # weird country representation
    if country_name == 'Czechia':
        country_name = 'Czech Republic'

    countries.append(country_name)

cols_name = ['Country']
cols = [countries]
write_csv('countries.csv', cols_name, cols)

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

root_url = "http://ontheworldmap.com/all/cities/"

page = requests.get(root_url)
soup = BeautifulSoup(page.content, "html.parser")

cities_cols = soup.find_all('div', class_='col-3')
paranthesis = re.compile(r'\([^)]*\)')

cities = set()

for cities_col in cities_cols[:3]:
    for city_row in cities_col.find_all('li'):
        city_name = city_row.find('a').text 
        city_name = re.sub(paranthesis, '', city_name).strip()
        
        cities.add(city_name)

cols_name = ['City']
cols = [cities]
write_csv('cities.csv', cols_name, cols)

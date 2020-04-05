from datetime import date
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag as bs4Tag

import re
import csv
import sys
import json
import os
import glob
import pandas as pd

sys.path.append('../../../helpers')
from helpers import write_csv

root_url = "https://www.uefa.com/uefachampionsleague/news/0252-0e9902dd97ae-bd3c7b568287-1000--champions-league-2018-19-all-the-fixtures-and-results/"

home_teams = []
away_teams = []
home_scores = []
away_scores = []
winners = []
stages = []
stage_winners = []
dates = []

stages_list = ['Group', "RoundOf16", "QuarterFinal", "SemiFinal", "Final"]

page = requests.get(root_url)
soup = BeautifulSoup(page.content, "lxml")
tag = soup.find('div', class_='article_body')

def add_to_lists(tag, stage, date):
	match = tag.text.strip()
	advancing = None
	going_next = None
	if '(' in match:
		tokens = match.split('(')
		new_tokens = tokens[1].split(" ")
		if 'win' in tokens[1]:
			for index in range(len(new_tokens)):
				if new_tokens[index] == 'win':
					going_next = new_tokens[index - 1]
					break
		else:
			for index in range(len(new_tokens)):
				if 'agg' in new_tokens[index]:
					score = new_tokens[index + 1]
					break
			if score[-1] == ")":
				score = score[:-1]
			score = score.strip().split("-")
			if int(score[0]) > int(score[1]):
				advancing = "first"
			else:
				advancing = "second"
		match = tokens[0].strip()

	# print (match)
	tokens = match.split(" ")
	first_team = True
	home_team = ""
	away_team = ""
	for token in tokens:
		if "-" in token and len(token) <= 5:
			score = token.split("-")
			home_score = score[0]
			away_score = score[1]
			first_team = False
			continue
		if first_team:
			home_team += token
			home_team += " "
		else:
			away_team += token
			away_team += " "

	home_team = home_team.strip()
	away_team = away_team.strip()
	if int(home_score) == int(away_score):
		winner = "Draw"
	elif int(home_score) > int(away_score):
		winner = "HomeTeam"
	else:
		winner = "AwayTeam"

	home_teams.append(home_team)
	away_teams.append(away_team)
	home_scores.append(home_score)
	away_scores.append(away_score)
	winners.append(winner)
	stages.append(stage)
	dates.append(date)
	if advancing == "first":
		stage_winners.append(home_team)
	elif advancing == "second":
		stage_winners.append(away_team)
	elif going_next != None:
		if going_next in home_team:
			stage_winners.append(home_team)
		else:
			stage_winners.append(away_team)
	else:
		stage_winners.append('-')


GROUP_ROUNDS = 6
DAY_GROUP_MATCHES = 8
DAYS = 2

stage = stages_list[0]
for i in range(GROUP_ROUNDS):
	tag = tag.findNext('h4')
	tag = tag.findNext('div').findNext('div')
	for k in range (DAYS):
		tag = tag.findNext('p')
		tag = tag.findNext('strong')
		date = tag.text.strip()
		for j in range(DAY_GROUP_MATCHES):
			tag = tag.findNext('a')
			add_to_lists(tag, stage, date)

def add_elements(tag, counter1, counter2, counter3):
	for k in range(counter1):
		tag = tag.findNext('h4')
		for i in range(counter2):
			tag = tag.findNext('p')
			tag = tag.findNext('strong')
			date = tag.text.strip()
			for j in range(counter3):
				tag = tag.findNext('a')
				add_to_lists(tag, stage, date)
	return tag

stage = stages_list[1]
tag = add_elements(tag, 2, 4, 2)

stage = stages_list[2]
tag = add_elements(tag, 2, 2, 2)

stage = stages_list[3]
tag = add_elements(tag, 2, 2, 1)

stage = stages_list[4]
tag = tag.findNext('h4').findNext('p')
date = tag.text.strip().split(':')[0]
tag = tag.findNext('a')
add_to_lists(tag, stage, date)

cols_name = ['HomeTeam', 'AwayTeam', 'HomeScore', 'AwayScore', 'Winner',
	'Stage', 'ToNextStage', "Date"]
cols = [home_teams, away_teams, home_scores, away_scores, winners, stages, stage_winners, dates]
write_csv('ChampionsLeague2018_2019.csv', cols_name, cols)



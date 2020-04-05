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

root_url = "https://www.uefa.com/uefachampionsleague/news/0252-0d047f2e3b30-2ef67bde4bc4-1000--all-the-2017-18-champions-league-results/"

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
	# match = tag.text.strip()
	match = tag

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

def add_elements(tag, counter1, counter2, counter3):
	for k in range(counter1):
		tag = tag.findNext('h4').findNext('p')
		for i in range(counter2):
			tag = tag.findNext('strong')
			date = tag.text.strip()
			if date[-1] == ':':
				date = date[:-1]
			for j in range(counter3):
				tag = tag.findNext('a')
				add_to_lists(tag.text.strip(), stage, date)
	return tag

GROUP_ROUNDS = 6
NO_GROUPS = 8

old_tag = tag

for i in range(9):
	tag = tag.findNext('h4')

stage = stages_list[0]
for i in range(GROUP_ROUNDS):
	tag = tag.findNext('h4')
	match_day = tag.text.strip()
	tag = tag.findNext('p')

	for k in range(NO_GROUPS):
		date = "-"
		tag = tag.findNext('strong')
		tag_name = tag.text.strip();
		for j in range(2):
			tag = tag.findNext('a')
			if tag_name == "Group E" and match_day == "Matchday three":
				if tag.text.split(" ")[0] == "Maribor":
					match = tag.text.strip() + " "
					tag = tag.findNext('a')
					match += tag.text.strip()
					add_to_lists(match, stage, date)
				else:
					add_to_lists(tag.text.strip(), stage, date)
			else:
				add_to_lists(tag.text.strip(), stage, date)

tag = old_tag
for i in range(6):
	tag = tag.findNext('h4')
stage = stages_list[1]
add_elements(tag, 2, 4, 2)

tag = old_tag
for i in range(4):
	tag = tag.findNext('h4')
stage = stages_list[2]
add_elements(tag, 2, 2, 2)

tag = old_tag
for i in range(2):
	tag = tag.findNext('h4')
stage = stages_list[3]
add_elements(tag, 2, 2, 1)

tag = old_tag
for i in range(1):
	tag = tag.findNext('h4')
stage = stages_list[4]
add_elements(tag, 1, 1, 1)

cols_name = ['HomeTeam', 'AwayTeam', 'HomeScore', 'AwayScore', 'Winner',
	'Stage', 'ToNextStage', "Date"]
cols = [home_teams, away_teams, home_scores, away_scores, winners, stages, stage_winners, dates]
write_csv('ChampionsLeague2017_2018.csv', cols_name, cols)



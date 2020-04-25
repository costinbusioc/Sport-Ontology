import pandas as pd
import os

from rdflib import Graph
from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF, FOAF
from datetime import datetime

month_to_date = {
	'Jan' : 1,
 	'Feb' : 2,
	'Mar' : 3,
	'Apr' : 4,
	'May' : 5,
	'Jun' : 6,
	'Jul' : 7,
	'Aug' : 8,
	'Sep' : 9, 
	'Oct' : 10,
	'Nov' : 11,
	'Dec' : 12
}

root = '../Ontologie/'
input_ontology = root + 'new_ontology.owl'
output_ontology = root + 'new_ontology.owl'

ontology_root = "http://purl.org/sport/ontology/"
dbpedia_root = "http://dbpedia.org/ontology/"

sport_ontology = Namespace(ontology_root)
dbpedia = Namespace(dbpedia_root)

g = Graph()

g.parse(input_ontology, format = "xml")

directory = "Campionate/"
tournaments = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.csv'):
            tournaments.append(file)

finals_stadiums = 'finals_stadiums.csv'
stadiums = {}
cities = {}
countries = {}
df = pd.read_csv(finals_stadiums)
for idx, row in df.iterrows():
	stadiums[row['Tournament']] = row['Stadium']
	cities[row['Tournament']] = row['City']
	countries[row['Tournament']] = row['Country']

no_rows = 0

for tournament in tournaments:
	tournament_name = tournament.replace("!", "/")
	tournament_URI = URIRef(ontology_root + tournament_name.replace("/", ":")[:-4])
	g.add((tournament_URI, RDF.type, sport_ontology.LeagueTournament))
	g.add((tournament_URI, sport_ontology.hasSportType, sport_ontology.Football))

	df = pd.read_csv(directory + tournament_name.replace("/", "!"))
	df.fillna('9999', inplace=True)
	for idx, row in df.iterrows():
		try:
			home_team = row['HomeTeam'].replace("/","")
			away_team = row['AwayTeam'].replace("/","")
			home_score = row['HomeScore']
			away_score = row['AwayScore']
			stage = row['Stage']
			date = row['Date']
			winner = row['Winner']

			if home_team == "9999"or away_team == "9999" or home_score == "9999" or away_score == "9999" or \
				stage == "9999" or date == "9999" or winner == "9999":
				continue

			match_URI = URIRef(ontology_root + home_team.replace(' ','_') + "=" + \
				away_team.replace(' ','_') + ":" + tournament_name.replace("/", ":")[:-4] + \
				date.replace(",", "").replace(" ","-"))
			home_team_URI = URIRef(ontology_root + home_team.replace(' ','_'))
			away_team_URI = URIRef(ontology_root + away_team.replace(' ','_'))

			g.add((match_URI, RDF.type, sport_ontology.Match))
			g.add((home_team_URI, RDF.type, sport_ontology.MultiPlayer))
			g.add((away_team_URI, RDF.type, sport_ontology.MultiPlayer))

			g.add((match_URI, sport_ontology.hasMatchName, Literal(home_team + " - "  + away_team)))
			g.add((match_URI, sport_ontology.hasHomeTeam, home_team_URI))
			g.add((match_URI, sport_ontology.hasAwayTeam, away_team_URI))
			g.add((match_URI, sport_ontology.hasHomeScore, Literal(home_score)))
			g.add((match_URI, sport_ontology.hasAwayScore, Literal(away_score)))
			g.add((match_URI, sport_ontology.hasTournament, tournament_URI))

			date_tokens = date.replace(",", "").split(" ")
			if len(date_tokens) == 3:
				date_ = datetime(int(date_tokens[2]), int(month_to_date[date_tokens[0]]), int(date_tokens[1]))
				g.add((match_URI, sport_ontology.hasDate, Literal(date_)))

			if stage == 'Final':
				stadium_URI = URIRef(ontology_root + stadiums[tournament_name[:-4]].replace(' ','_'))
				g.add((stadium_URI, RDF.type, dbpedia.Stadium))
				g.add((stadium_URI, dbpedia.informationName, Literal(stadiums[tournament_name[:-4]])))

				city_URI = URIRef(ontology_root + cities[tournament_name[:-4]].replace(' ','_'))
				g.add((city_URI, RDF.type, dbpedia.City))
				g.add((city_URI, dbpedia.informationName, Literal(cities[tournament_name[:-4]])))

				country_URI = URIRef(ontology_root + countries[tournament_name[:-4]].replace(' ','_'))
				g.add((country_URI, RDF.type, dbpedia.City))
				g.add((country_URI, dbpedia.informationName, Literal(countries[tournament_name[:-4]])))

				g.add((match_URI, sport_ontology.hasLocation, country_URI))
				g.add((match_URI, sport_ontology.hasLocation, city_URI))
				g.add((match_URI, sport_ontology.hasLocation, stadium_URI))

			if 'StageWinner' in row:
				stage_winner = row['StageWinner']
				if stage_winner != "-":
					if stage_winner == home_team:
						g.add((match_URI, sport_ontology.hasStageWinner, home_team_URI))
					else:
						g.add((match_URI, sport_ontology.hasStageWinner, away_team_URI))
		
			g.add((match_URI, sport_ontology.hasStage, Literal(stage)))

			no_rows += 1
		except:
			continue

print (no_rows)
g.serialize(destination=output_ontology, format="xml")


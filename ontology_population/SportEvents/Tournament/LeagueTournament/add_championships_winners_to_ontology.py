import pandas as pd

from rdflib import Graph
from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF, FOAF
from datetime import datetime

input_table_list = ['championship_winners.csv',
			   		'championsLeague_winners.csv',
			   		'europaLeague_winners.csv']

root = '../Ontologie/'
input_ontology = root + 'new_ontology.owl'
output_ontology = root + 'new_ontology.owl'

ontology_root = "http://purl.org/sport/ontology/"
dbpedia_root = "http://dbpedia.org/ontology/"

sport_ontology = Namespace(ontology_root)
dbpedia = Namespace(dbpedia_root)

g = Graph()

g.parse(input_ontology, format = "xml")

no_rows = 0

for input_table in input_table_list:
	df = pd.read_csv(input_table)
	df.fillna('9999', inplace=True)
	if input_table == 'championsLeague_winners.csv' or input_table == 'europaLeague_winners.csv':
		for idx, row in df.iterrows():
			try:
				champion_name = row['ChampionshipWinner']
				championship_name = row['Championship']
				manager = row['CoachWinner']
				season = row['Season']

				if champion_name == "9999" or championship_name == "9999" or manager == "9999" or season == "9999":
					continue

				if championship_name.split('_')[1].split("/")[0] == "1999":
					championship_name = championship_name[:-4] + "2000"

				start_date = championship_name.split("_")[1].split("/")[0]
				end_date = championship_name.split("_")[1].split("/")[0]
				start_date = datetime(int(start_date), 9, 1)
				end_date = datetime(int(end_date), 5, 31)

				champion_URI = URIRef(ontology_root + champion_name.replace(' ','_'))
				championship_URI = URIRef(ontology_root + championship_name.replace("/",":"))

				g.add((champion_URI, RDF.type, sport_ontology.MultiPlayer))
				g.add((championship_URI, RDF.type, sport_ontology.LeagueTournament))

				g.add((champion_URI, sport_ontology.hasTeamName, Literal(champion_name)))
				g.add((championship_URI, dbpedia.champion, champion_URI))
				g.add((championship_URI, sport_ontology.hasTournamentName, Literal(championship_name.split("_")[0])))
				g.add((championship_URI, sport_ontology.hasSportType, sport_ontology.Football))

				g.add((championship_URI, dbpedia.startDateTime, Literal(start_date)))
				g.add((championship_URI, dbpedia.endDateTime, Literal(end_date)))

				if len(manager) > 3:
					manager_URI = URIRef(ontology_root + manager.replace(' ','_'))
					g.add((manager_URI, RDF.type, sport_ontology.Manager))
					g.add((manager_URI, FOAF.name, Literal(manager)))

				no_rows += 1
			except:
				continue
	else:
		for idx, row in df.iterrows():
			try:
				champion_name = row['ChampionshipWinner']
				championship_name = row['Championship']
				country = row['Country']
				manager = row['CoachWinner']
				season = row['Season']

				if champion_name == "9999" or championship_name == "9999" or manager == "9999" or season == "9999" or country == "9999":
					continue

				if championship_name.split('_')[1].split("/")[0] == "1999":
					championship_name = championship_name[:-4] + "2000"

				start_date = championship_name.split("_")[1].split("/")[0]
				end_date = championship_name.split("_")[1].split("/")[1]
				start_date = datetime(int(start_date), 9, 1)
				end_date = datetime(int(end_date), 5, 31)

				champion_URI = URIRef(ontology_root + champion_name.replace(' ','_'))
				championship_URI = URIRef(ontology_root + championship_name.replace("/",":"))
				country_URI = URIRef(ontology_root + country.replace(' ','_'))

				g.add((champion_URI, RDF.type, sport_ontology.MultiPlayer))
				g.add((country_URI, RDF.type, dbpedia.Country))
				g.add((championship_URI, RDF.type, sport_ontology.LeagueTournament))

				g.add((champion_URI, sport_ontology.hasTeamName, Literal(champion_name)))
				g.add((championship_URI, dbpedia.champion, champion_URI))
				g.add((championship_URI, sport_ontology.hasLocation, country_URI))
				g.add((championship_URI, sport_ontology.hasTournamentName, Literal(championship_name.split("_")[0])))
				g.add((championship_URI, sport_ontology.hasSportType, sport_ontology.Football))

				g.add((championship_URI, dbpedia.startDateTime, Literal(start_date)))
				g.add((championship_URI, dbpedia.endDateTime, Literal(end_date)))
		
				if len(manager) > 3:
					manager_URI = URIRef(ontology_root + manager.replace(' ','_'))
					g.add((manager_URI, RDF.type, sport_ontology.Manager))
					g.add((manager_URI, FOAF.name, Literal(manager)))

				no_rows += 1
			except:
				continue

print (no_rows)
g.serialize(destination=output_ontology, format="xml")


import pandas as pd

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

input_table = 'active_players.csv'
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

df = pd.read_csv(input_table)
print (df.shape)
df.fillna('9999', inplace=True)
for idx, row in df.iterrows():
	try:
		player_name = row['PlayerName']
		player_nationality = row['Nationality']
		birthdate = row['Birthdate']
		position = row['Position']
		club = row['Club'].replace("/", "")
		captain = row['Captain']

		if player_name == "9999" or player_nationality == "9999" or birthdate == "9999" or position == "9999" or club == "9999" or captain == "9999":
			continue

		player_URI = URIRef(ontology_root + player_name.replace(' ','_'))
		nationality_URI = URIRef(ontology_root + player_nationality.replace(' ','_'))
		club_URI = URIRef(ontology_root + club.replace(' ','_'))

		g.add((player_URI, RDF.type, sport_ontology.FootballPlayer))
		g.add((nationality_URI, RDF.type, dbpedia.Country))
		g.add((club_URI, RDF.type, sport_ontology.MultiPlayer))

		g.add((player_URI, FOAF.name, Literal(player_name)))
		g.add((club_URI, sport_ontology.hasTeamName, Literal(club)))
		g.add((nationality_URI, dbpedia.informationName, Literal(player_nationality)))
		g.add((player_URI, dbpedia.playerInTeam, club_URI))
		g.add((player_URI, sport_ontology.hasGender, Literal('Male')))

		g.add((player_URI, sport_ontology.hasNationality, nationality_URI))
		tokens = birthdate.replace(',', '').split(' ')
		birthdate = datetime(int(tokens[2]), month_to_date[tokens[0]], int(tokens[1]))
		g.add((player_URI, sport_ontology.hasBirthdate, Literal(birthdate)))
		g.add((player_URI, sport_ontology.playerPosition, Literal(position)))
		
		if captain == "Team captain":
			g.add((club_URI, sport_ontology.hasCaptain, player_URI))

		no_rows += 1
	except:
		continue

print (no_rows)
g.serialize(destination=output_ontology, format="xml")


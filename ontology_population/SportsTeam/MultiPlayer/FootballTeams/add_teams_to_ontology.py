import pandas as pd

from rdflib import Graph
from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF, FOAF

input_table = 'teams.csv'
root = '../Ontologie/'
input_ontology = root + 'ontology.owl'
output_ontology = root + 'new_ontology.owl'

ontology_root = "http://purl.org/sport/ontology/"
dbpedia_root = "http://dbpedia.org/ontology/"
foaf_root = "http://xmlns.com/foaf/0.1/"

sport_ontology = Namespace(ontology_root)
dbpedia = Namespace(dbpedia_root)
foaf = Namespace(foaf_root)

g = Graph()

g.parse(input_ontology, format = "xml")

no_rows = 0

df = pd.read_csv(input_table)
df.fillna('9999', inplace=True)
for idx, row in df.iterrows():
	try:
		team_name = row['TeamName'].replace("/", "")
		country = row['Country']
		coach = row['Coach']
		stadium = row['Stadium'].replace("/", "")
		stadium_capacity = row['StadiumCapacity']

		if team_name == "9999" or country == "9999" or coach == "9999" or stadium == "9999" or stadium_capacity == "9999":
			continue

		team_name_URI = URIRef(ontology_root + team_name.replace(' ','_'))
		country_URI = URIRef(ontology_root + country.replace(' ','_'))
		coach_URI = URIRef(ontology_root + coach.replace(' ','_') + "_manager")

		g.add((team_name_URI, RDF.type, sport_ontology.MultiPlayer))
		g.add((country_URI, RDF.type, dbpedia.Country))
		g.add((country_URI, dbpedia.informationName, Literal(country)))

		if len(coach) > 4:
			g.add((coach_URI, RDF.type, sport_ontology.Manager))
			g.add((coach_URI, FOAF.name, Literal(coach)))
			g.add((coach_URI, sport_ontology.hasGender, Literal('Male')))
			g.add((team_name_URI, dbpedia.manager, coach_URI))

		g.add((team_name_URI, sport_ontology.hasTeamName, Literal(team_name)))
		g.add((team_name_URI, sport_ontology.hasClubLocation, country_URI))

		if 'Matchday' not in stadium and len(stadium) > 3 \
			and '"' not in stadium and '|' not in stadium:
			stadium_URI = URIRef(ontology_root + stadium.replace(' ','_'))
			g.add((stadium_URI, RDF.type, dbpedia.Stadium))
			g.add((stadium_URI, dbpedia.informationName, Literal(stadium)))
			g.add((team_name_URI, sport_ontology.hasClubLocation, stadium_URI))

			if 'Seats' in stadium_capacity:
				stadium_capacity = stadium_capacity.split(" ")[0]
				tokens = stadium_capacity.split(".")
				if len(stadium_capacity) >= 4:
					stadium_capacity = tokens[0] + tokens[1]
					g.add((stadium_URI, sport_ontology.hasCapacity, Literal(stadium_capacity)))

		no_rows += 1
	except:
		continue

print (no_rows)
g.serialize(destination=output_ontology, format="xml")
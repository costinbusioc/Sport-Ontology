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

def old_country_to_new_one(country):
	if country == "UdSSR":
		return "Ukraine"
	elif country == "Jugoslawien (SFR)":
		return "Bosnia-Herzegovina"
	elif country == "CSSR":
		return "Czech Republic"
	elif country == "DDR":
		return "Germany"
	return country

input_table_list = ['2_retired_players_history.csv',
					'retired_players_history.csv',
					'active_players_history.csv']

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
	print (df.shape)
	for idx, row in df.iterrows():
		try:
			player_name = row['PlayerName'].replace("`","")
			joinedTeam = row['JoinedTeam'].replace("/", "")
			leftTeam = row['LeftTeam'].replace("/", "")
			joinDate = row['JoinDate']
			endDate = row['EndDate']
			transfer_value = row['Value']
			season = row['Season']

			if player_name == "9999" or joinedTeam == "9999" or leftTeam == "9999" or joinDate == "9999" or endDate == "9999" or \
				transfer_value == "9999" or season == "9999":
				continue

			transfer_name = ontology_root + player_name.replace(' ','_') + \
				":" + leftTeam.replace(' ','_') + \
				":" + joinedTeam.replace(' ','_') + \
				":" + season.replace("/", ":")
			transfer_URI = URIRef(transfer_name)
			player_URI = URIRef(ontology_root + player_name.replace(' ','_'))
			joinedTeam_URI = URIRef(ontology_root + joinedTeam.replace(' ','_'))
			leftTeam_URI = URIRef(ontology_root + leftTeam.replace(' ','_'))

			g.add((transfer_URI, RDF.type, sport_ontology.Transfer))
			g.add((player_URI, RDF.type, sport_ontology.FootballPlayer))
			g.add((joinedTeam_URI, RDF.type, sport_ontology.MultiPlayer))
			g.add((leftTeam_URI, RDF.type, sport_ontology.MultiPlayer))

			g.add((transfer_URI, sport_ontology.hasPerson, player_URI))
			g.add((player_URI, FOAF.name, Literal(player_name)))
			g.add((transfer_URI, sport_ontology.hasTeam, joinedTeam_URI))

			g.add((joinedTeam_URI, sport_ontology.hasTeamName, Literal(joinedTeam)))
			g.add((leftTeam_URI, sport_ontology.hasTeamName, Literal(leftTeam)))

			if len(joinDate) > 4:
				tokens = joinDate.replace(",","").split(" ")
				joinDate = datetime(int(tokens[2]), int(month_to_date[tokens[0]]), int(tokens[1]))
				g.add((transfer_URI, sport_ontology.hasStartDate, Literal(joinDate)))

			if len(endDate) > 4:
				tokens = endDate.replace(",","").split(" ")
				endDate = datetime(int(tokens[2]), int(month_to_date[tokens[0]]), int(tokens[1]))
				g.add((transfer_URI, sport_ontology.hasEndDate, Literal(endDate)))

			if isinstance(transfer_value, str) and len(transfer_value) > 4:
				g.add((transfer_URI, sport_ontology.hasDetails, Literal(transfer_value)))

			if 'retired' in input_table:
				nationality = row['Nationality']
				country_left_team = row['CountryLeftTeam']
				country_joined_team = row['CountryJoinedTeam']

				nationality = old_country_to_new_one(nationality)
				country_left_team = old_country_to_new_one(country_left_team)
				country_joined_team = old_country_to_new_one(country_joined_team)

				if nationality != "-":
					nationality_URI = URIRef(ontology_root + nationality.replace(' ','_'))
					g.add((nationality_URI, RDF.type, dbpedia.Country))
					g.add((nationality_URI, dbpedia.informationName, Literal(nationality)))
					g.add((player_URI, sport_ontology.hasNationality, nationality_URI))

				if country_left_team != "-":
					country_left_team_URI = URIRef(ontology_root + country_left_team.replace(' ','_'))
					g.add((country_left_team_URI, RDF.type, dbpedia.Country))
					g.add((country_left_team_URI, dbpedia.informationName, Literal(country_left_team)))
					g.add((leftTeam_URI, sport_ontology.teamInCountry, country_left_team_URI))
				
				if country_joined_team != "-":
					country_joined_team_URI = URIRef(ontology_root + country_joined_team.replace(' ','_'))
					g.add((country_joined_team_URI, RDF.type, dbpedia.Country))
					g.add((country_joined_team_URI, dbpedia.informationName, Literal(country_joined_team)))
					g.add((joinedTeam_URI, sport_ontology.teamInCountry, country_joined_team_URI))
		
			no_rows += 1
		except:
			continue

print (no_rows)

g.serialize(destination=output_ontology, format="xml")


import pandas as pd
import math

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

input_table_list = ['retired_managers_history.csv',
					'active_managers_history.csv',
					'2_retired_managers_history.csv']

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
			manager_name = row['ManagerName']
			manager_nationality = row['Nationality']
			club = row['WorkedInClub'].replace("/", "")
			if 'CountryClub' in row:
				country = row['CountryClub']
			else:
				country = row['Country']
			begin = row['FromDate']
			end = row['ToDate']
			position = row['Position']

			if manager_name == "9999" or manager_nationality == "9999" or club == "9999" or begin == "9999" or \
				end == "9999" or position == "9999":
				continue

			old_begin = begin
			old_end = end
			url_begin = "-"
			url_end = "-"
			if '(' in begin:
				tokens = begin.replace('(','').replace(')','').replace(',', '').split(' ')
				begin = datetime(int(tokens[3]), int(month_to_date[tokens[1]]), int(tokens[2]))
				url_begin = tokens[2] + "-" + tokens[1] + "-" + tokens[3]
			if '(' in end:
				tokens = end.replace('(','').replace(')','').replace(',', '').split(' ')
				end = datetime(int(tokens[3]), int(month_to_date[tokens[1]]), int(tokens[2]))
				url_end = tokens[2] + "-" + tokens[1] + "-" + tokens[3]

			manager_job_name = manager_name.replace(' ','_') + \
				":" + club.replace(' ','_') + ":" + url_begin + ":" + url_end
			manager_job_URI = URIRef(ontology_root + manager_job_name)
			manager_name_for_URI = manager_name.replace(' ','_') + "_manager"
			manager_URI = URIRef(ontology_root + manager_name_for_URI)
			club_URI = URIRef(ontology_root + club.replace(' ','_'))
			country_URI = URIRef(ontology_root + country.replace(' ','_'))

			if len (manager_nationality) > 4:
				nationality_URI = URIRef(ontology_root + manager_nationality.replace(' ','_'))
				g.add((nationality_URI, RDF.type, dbpedia.Country))
				g.add((nationality_URI, dbpedia.informationName, Literal(manager_nationality)))
				g.add((manager_URI, sport_ontology.hasNationality, nationality_URI))
				
			g.add((manager_job_URI, RDF.type, sport_ontology.Transfer))
			g.add((club_URI, RDF.type, sport_ontology.MultiPlayer))
			g.add((manager_URI, RDF.type, sport_ontology.Manager))
			g.add((country_URI, RDF.type, dbpedia.Country))	

			g.add((manager_job_URI, sport_ontology.hasPerson, manager_URI))
			g.add((manager_job_URI, sport_ontology.hasTeam, club_URI))
			g.add((manager_job_URI, sport_ontology.hasDetails, Literal(position)))

			if '(' in old_begin:
				g.add((manager_job_URI, sport_ontology.hasStartDate, Literal(begin)))

			if '(' in old_end:
				g.add((manager_job_URI, sport_ontology.hasEndDate, Literal(end)))

			g.add((manager_URI, FOAF.name, Literal(manager_name)))
			g.add((club_URI, sport_ontology.hasTeamName, Literal(club)))
			g.add((country_URI, dbpedia.informationName, Literal(country)))
			g.add((club_URI, sport_ontology.hasClubLocation, country_URI))
		
			no_rows += 1;
		except:
			continue

print (no_rows)

g.serialize(destination=output_ontology, format="xml")
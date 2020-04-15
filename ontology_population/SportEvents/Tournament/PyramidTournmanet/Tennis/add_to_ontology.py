import pandas as pd
from datetime import datetime, timedelta

from rdflib import Graph
from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF, FOAF

input_tables = ['1975-2005_tennis_tournaments.csv', '2005-2015_tournaments.csv', '2015-2019_tournaments.csv']
input_ontology = 'ontology.owl'
output_ontology = 'ontology.owl'

ontology_root = "http://purl.org/sport/ontology/"
dbpedia_root = "http://dbpedia.org/ontology/"

sports_ontology = Namespace(ontology_root)
dbpedia = Namespace(dbpedia_root)

g = Graph()

g.parse(input_ontology, format="xml")

for input_table in input_tabls:
    df = pd.read_csv(input_table)
    for idx, row in df.iterrows():
        champion_name = row['Champion']
        cal_year = row['Year']
        name = row['Tournament']
        startDate = row['Start Date']
        city = row['City']
        country = row['Country']
        surface = row['Surface']
        prize = row['Prize']

        year, month, day = startDate.split('.')
        startDate = datetime(int(year), int(month), int(day))
        endDate = startDate + timedelta(days=7)

        if name == 'US Open' or name == 'Wimbledon' or name == 'Australian Open' or name == 'Roland Garros':
            endDate += timedelta(days=7)
        if country == 'Great Britain':
            country = 'United Kingdom'
        if country == 'United States':
            country = 'United States of America'
        if city == 'New York':
            city = 'New York City'
        if city == 'Washington':
            city = 'Washington D.C.'

        tournament_URI = URIRef(ontology_root + name.replace(' ' , '_') + str(cal_year))
        champion_URI = URIRef(ontology_root + champion_name.replace(' ', '_') + 'SinglePlayerTeam')
        if country != 'Empty':
            country_URI = URIRef(ontology_root + country.replace(' ', '_'))
        
        try:
            city_URI = URIRef(ontology_root + city.replace(' ', '_'))
        except:
            continue

        g.add((tournament_URI, RDF.type, sports_ontology.PyramidTournament))
        g.add((tournament_URI, sports_ontology.hasTournamentName, Literal(name)))
        g.add((tournament_URI, dbpedia.startDateTime, Literal(startDate)))
        g.add((tournament_URI, dbpedia.endDateTime, Literal(endDate)))
        g.add((tournament_URI, dbpedia.champion, champion_URI))
        if country != 'Empty':
            g.add((tournament_URI, sports_ontology.hasLocation, country_URI))
        g.add((tournament_URI, sports_ontology.hasLocation, city_URI))
        g.add((tournament_URI, sports_ontology.hasSurface, Literal(surface)))
        g.add((tournament_URI, sports_ontology.hasPrize, Literal(prize)))
        g.add((tournament_URI, sports_ontology.hasSportType, sports_ontology.Tennis))



g.serialize(destination=output_ontology, format="xml")

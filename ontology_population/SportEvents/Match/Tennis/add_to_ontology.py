import pandas as pd
from datetime import datetime, timedelta

from rdflib import Graph
from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF, FOAF

input_tables = ['1975-1983_tennis_matches.csv', '1984-2004_tennis_matches.csv', '2005-2013_tennis_matches.csv', '2004_tennis_matches.csv', '2015-2019_tennis_matches.csv']
input_ontology = 'ontology.owl'
output_ontology = 'ontology.owl'

ontology_root = "http://purl.org/sport/ontology/"
dbpedia_root = "http://dbpedia.org/ontology/"

sports_ontology = Namespace(ontology_root)
dbpedia = Namespace(dbpedia_root)

g = Graph()

g.parse(input_ontology, format="xml")

for input_table in input_tables:
    df = pd.read_csv(input_table)
    for idx, row in df.iterrows():
        cal_year = row['Year']
        tournament = row['Tournament']
        city = row['City']
        country = row['Country']
        home_player = row['Home']
        away_player = row['Away']
        home_score = row['Home Score']
        away_score = row['Away Score']

        if country == 'Great Britain':
            country = 'United Kingdom'
        if country == 'United States':
            country = 'United States of America'
        if city == 'New York':
            city = 'New York City'
        if city == 'Washington':
            city = 'Washington D.C.'

        match_URI = URIRef(ontology_root + home_player.replace(' ' , '_') + '-' + away_player.replace(' ', '_') + tournament.replace(' ', '_') + str(cal_year))
        home_URI = URIRef(ontology_root + home_player.replace(' ', '_') + 'SinglePlayerTeam')
        away_URI = URIRef(ontology_root + away_player.replace(' ', '_') + 'SinglePlayerTeam')
        tournament_URI = URIRef(ontology_root + tournament.replace(' ' , '_') + str(cal_year))
        if country != 'Empty':
            country_URI = URIRef(ontology_root + country.replace(' ', '_'))
        try:
            city_URI = URIRef(ontology_root + city.replace(' ', '_'))
        except:
            continue

        g.add((match_URI, RDF.type, sports_ontology.Match))
        g.add((match_URI, sports_ontology.hasMatchName, Literal(home_player + ' - ' + away_player)))
        g.add((match_URI, sports_ontology.hasHomeScore, Literal(home_score)))
        g.add((match_URI, sports_ontology.hasAwayScore, Literal(away_score)))
        g.add((match_URI, sports_ontology.hasTournament, tournament_URI))
        if country != 'Empty':
            g.add((match_URI, sports_ontology.hasLocation, country_URI))
        g.add((match_URI, sports_ontology.hasLocation, city_URI))
        g.add((tournament_URI, sports_ontology.hasSportType, sports_ontology.Tennis))
        g.add((match_URI, sports_ontology.hasHomeTeam, home_URI))
        g.add((match_URI, sports_ontology.hasAwayTeam, away_URI))

g.serialize(destination=output_ontology, format="xml")

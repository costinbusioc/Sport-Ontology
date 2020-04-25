import pandas as pd

from rdflib import Graph
from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF, FOAF

input_tables = ['new_tennis_players.csv', '2005_2015_new_players.csv', '2015_2020_players.csv'] 
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
        tennis_player_name = row['Name']
        tennis_player_URI = URIRef(ontology_root + tennis_player_name.replace(' ', '_'))
        
        g.add((tennis_player_URI, RDF.type, dbpedia.TennisPlayer))
        g.add((tennis_player_URI, FOAF.name, Literal(tennis_player_name)))
        g.add((tennis_player_URI, sports_ontology.hasGender, Literal('Male')))

    g.serialize(destination=output_ontology, format="xml")

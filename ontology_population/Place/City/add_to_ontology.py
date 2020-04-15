import pandas as pd

from rdflib import Graph
from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF, FOAF

input_table = 'cities.csv'
input_ontology = 'ontology.owl'
output_ontology = 'new_ontology.owl'

ontology_root = "http://purl.org/sport/ontology/"
dbpedia_root = "http://dbpedia.org/ontology/"

sports_ontology = Namespace(ontology_root)
dbpedia = Namespace(dbpedia_root)

g = Graph()

g.parse(input_ontology, format="xml")

df = pd.read_csv(input_table)
for idx, row in df.iterrows():
    city_name = row['City']
    city_URI = URIRef(ontology_root + city_name.replace(' ', '_'))
    
    g.add((city_URI, RDF.type, dbpedia.City))
    g.add((city_URI, dbpedia.informationName, Literal(city_name)))

g.serialize(destination=output_ontology, format="xml")

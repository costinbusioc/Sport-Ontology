import pandas as pd

from rdflib import Graph
from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF, FOAF

input_table = 'countries.csv'
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
    country_name = row['Country']
    country_URI = URIRef(ontology_root + country_name.replace(' ', '_'))
    
    g.add((country_URI, RDF.type, dbpedia.Country))
    g.add((country_URI, dbpedia.informationName, Literal(country_name)))

g.serialize(destination=output_ontology, format="xml")

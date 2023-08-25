from sparql_dataframe import get
from SPARQLWrapper import *
import json

endpoint = 'https://dati.cultura.gov.it/sparql'

query = """
SELECT DISTINCT ?material ?label ?materialNarrow ?label2 WHERE {
    <http://dati.beniculturali.it/vocabularies/opere_e_oggetti_d_arte_materia/def/> skos:hasTopConcept ?material.
    ?material rdfs:label ?label;
    skos:narrower ?materialNarrow.
    ?materialNarrow rdfs:label ?label2.
}
"""

client = SPARQLWrapper(endpoint)
client.setQuery(query)
client.setReturnFormat(JSON)
materialResults = client.query().convert()

with open("data/jsonMaterials.json", "w", encoding="utf-8") as f:
    json.dump(materialResults, f, indent=4)


query = """
SELECT DISTINCT ?technique ?label ?techniqueNarrow ?label2 WHERE {
    <http://dati.beniculturali.it/vocabularies/opere_e_oggetti_d_arte_tecnica/def/> skos:hasTopConcept ?technique.
    ?technique rdfs:label ?label;
    skos:narrower ?techniqueNarrow.
    ?techniqueNarrow rdfs:label ?label2.
}
"""

client.setQuery(query)
client.setReturnFormat(JSON)
techniqueResults = client.query().convert()
print(techniqueResults)

with open("data/jsonTechniques.json", "w", encoding="utf-8") as f:
    json.dump(techniqueResults, f, indent=4)
'''


query = """
SELECT DISTINCT ?material ?label ?materialNarrow ?label2 WHERE {
    <http://dati.beniculturali.it/vocabularies/opere_e_oggetti_d_arte_materia/def/> skos:hasTopConcept ?material.
    ?material rdfs:label ?label;
    skos:narrower ?materialNarrow.
    ?materialNarrow rdfs:label ?label2.
}
"""
df = get(endpoint, query)
print(df[0:10])

'''
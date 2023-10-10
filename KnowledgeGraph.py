from pandas import *
from rdflib import RDF, Graph, URIRef, RDFS, Literal, Namespace, OWL
from ast import literal_eval

from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore


#take the automatic- and manually- extracted data and merge them in one table
with open("data/data.csv", "r", encoding="utf-8") as f:
    extractedData = read_csv(f,keep_default_na=False, converters={"material": literal_eval, "technique": literal_eval})

with open("data/Dataset_paintings.csv", "r", encoding="utf-8") as f:
    otherData = read_csv(f, sep=";", keep_default_na=False)

data = merge(extractedData, otherData, left_on="identifier", right_on="ID", how="left")
data = data.drop(columns=["Author", "Artwork", "Artwork component", "Material", "Technique", "ID"]).fillna('')

#open blazegraph connection java -server -Xmx1g -jar blazegraph.jar
endpoint = "http://192.168.56.1:9999/blazegraph/sparql"

baseUrl = Namespace("https://github.com/Bianca-LM/art-criticism-ontology/mat/resource/")

directory = 'data'

#create an empty knowledge graph
knowledgeGraph = Graph()

knowledgeGraph.bind("mat-r", baseUrl)

mat = Namespace('https://github.com/Bianca-LM/art-criticism-ontology/mat')

knowledgeGraph.bind("mat", mat)

#Ontology = URIRef('https://github.com/Bianca-LM/art-criticism-ontology/mat/knowledge-graph/')

knowledgeGraph.add((URIRef('https://github.com/Bianca-LM/art-criticism-ontology/mat/resource/'), RDF.type, OWL.Ontology))
knowledgeGraph.add((URIRef('https://github.com/Bianca-LM/art-criticism-ontology/mat/resource/'), OWL.imports, URIRef('https://github.com/Bianca-LM/art-criticism-ontology/mat')))


for idx, row in data.iterrows():
    id = URIRef(baseUrl + row["identifier"])
    knowledgeGraph.add((id, RDF.type, mat.Artwork))
    author = URIRef(baseUrl + row["author"].replace(" ", "-"))
    knowledgeGraph.add((author, RDF.type, mat.Author))
    knowledgeGraph.add((id, mat.hasAuthor, author))
    knowledgeGraph.add((author, RDFS.Literal, Literal(row["author"])))
    knowledgeGraph.add((id, mat.hasTitle, Literal(row["title"])))
    for technique in row["technique"]: 
        techniqueURI = URIRef(baseUrl + row["identifier"] + "-" + technique)
        knowledgeGraph.add((id, mat.hasTechnique, techniqueURI)) 
        knowledgeGraph.add((techniqueURI, RDF.type, mat.Technique)) 
        knowledgeGraph.add((techniqueURI, RDFS.Literal, Literal(technique))) 
        for material in row["material"]: 
            materialURI = URIRef(baseUrl + row["identifier"] + "-" + material)
            #there it should be added a owl same as with the skos vocabulary
            knowledgeGraph.add((techniqueURI, mat.isPerformedOn, materialURI))
            knowledgeGraph.add((materialURI, RDF.type, mat.Material))
            knowledgeGraph.add((materialURI, RDFS.Literal, Literal(material))) 

    if row["Current support"] != '':
        currentSupport = URIRef(baseUrl + row["identifier"] + "-CurrentSupport-" + row["Current support"].replace(" ", "-"))
        knowledgeGraph.add((id, mat.hasCurrentSupport, currentSupport))  
        knowledgeGraph.add((currentSupport, RDF.type, mat.Support))
        knowledgeGraph.add((currentSupport, RDF.type, mat.Material))
        knowledgeGraph.add((currentSupport, RDFS.Literal, Literal(row["Current support"])))
        knowledgeGraph.add((currentSupport, mat.isCurrentSupportOf, id))
        if row["Previous support"] != '':
            previousSupport =  URIRef(baseUrl + row["identifier"] + "-PreviousSupport-" + row["Previous support"].replace(" ", "-")) 
            knowledgeGraph.add((currentSupport, mat.transferredFrom, previousSupport))
            knowledgeGraph.add((id, mat.hasPreviousSupport, previousSupport))
            knowledgeGraph.add((previousSupport, RDF.type, mat.Support))
            knowledgeGraph.add((previousSupport, RDF.type, mat.Material))
            knowledgeGraph.add((previousSupport, RDFS.Literal, Literal(row["Previous support"])))
            knowledgeGraph.add((previousSupport, mat.isPreviousSupportOf, id))
    if row["Decoration"] != '':
        knowledgeGraph.add((id, mat.hasDecoration, URIRef(baseUrl + "Decoration-" + row["identifier"])))
        knowledgeGraph.add((URIRef(baseUrl + "Decoration-" + row["identifier"]), RDF.type, mat.Decoration))
        knowledgeGraph.add((URIRef(baseUrl + "Decoration-" + row["identifier"]), RDFS.Literal, Literal(row["Decoration"])))
    if row["Ornament"] != '':
        knowledgeGraph.add((id, mat.hasOrnament, URIRef(baseUrl + "Ornament-" + "ornament-" + row["identifier"])))
        knowledgeGraph.add((URIRef(baseUrl + "Ornament-" + row["identifier"]), RDF.type, mat.Ornament))
        knowledgeGraph.add((URIRef(baseUrl + "Ornament-" + row["identifier"]), RDFS.Literal, Literal(row["Ornament"])))
    if row["Signature"] != '':
        knowledgeGraph.add((id, mat.hasSignature, URIRef(baseUrl + "Signature-" + row["identifier"])))
        knowledgeGraph.add((URIRef(baseUrl + "Signature-" + row["identifier"]), RDF.type, mat.Signature))
        knowledgeGraph.add((URIRef(baseUrl + "Signature-" + row["identifier"]), RDFS.Literal, Literal(row["Signature"])))
        if row["Signature datation"] != '':
            knowledgeGraph.add((mat.Signature, mat.isDated, URIRef(baseUrl + "SignatureDatation-" + row["identifier"])))
            knowledgeGraph.add((URIRef(baseUrl + "SignatureDatation-" + row["identifier"]), RDF.type, mat.Signature_Datation ))
            knowledgeGraph.add((URIRef(baseUrl + "SignatureDatation-" + row["identifier"]), RDFS.Literal, Literal(row["Signature datation"])))
    if row["Inscription"] != '':
        knowledgeGraph.add((id, mat.hasInscription, URIRef(baseUrl + "Inscription-" + row["identifier"])))
        knowledgeGraph.add((URIRef(baseUrl + "Inscription-" + row["identifier"]), RDF.type, mat.Inscription))
        knowledgeGraph.add((URIRef(baseUrl + "Inscription-" + row["identifier"]), RDFS.Literal, Literal(row["Inscription"])))

store = SPARQLUpdateStore()

store.open((endpoint, endpoint))


#Turtle serialization
ttl = knowledgeGraph.serialize(destination='knowledgeGraph.txt', format='turtle')

'''
#load into blazegraph
for triple in knowledgeGraph.triples((None, None, None)):
    try:
        store.add(triple)
    except: 
        print(triple)
    
store.close()
'''
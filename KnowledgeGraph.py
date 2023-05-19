from pandas import read_csv, Series
from rdflib import RDF, Graph, URIRef, RDFS, Literal, Namespace
import os

#All the Entities
Artwork = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Artwork')
ArtworkComponent = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Artwork_Component')
CurrentSupport = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Current_Support')
Decoration = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Decoration')
Frame = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Frame')
Inscription = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Inscription')
Mark = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Mark')
MarkOfCarter = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Mark_of_Carter')
MarkOfFounder = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Mark_of_Founder')
Material = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Material')
OriginalSupport = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Original_Support')
Ornament = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Ornament')
Signature = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Signature')
SignatureDatation = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Signature_Datation')
Support = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Support')
Technique = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#Technique')

#All the Object Properties
hasDecoration = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasDecoration')
hasFrame = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasFrame')
hasTechnique = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasTechnique')
hasDecorativeTechnique = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasDecorativeTechnique')
hasInscription = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasInscription')
hasOrnament = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasOrnament')
hasOrnamentalTechnique = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasOrnamentalTechnique')
hasSupport = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasSupport')
isDated = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#isDated')
isMadeOf = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#isMadeOf')
isMarked = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#isMarked')
isMountedOn = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#isMountedOn')
transferredFrom = URIRef('ttp://www.semanticweb.org/bianc/ontologies/2023/1/mat#transferredFrom')
isPerformedOn = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#isPerformedOn')
isSigned = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#isSigned')

#All the Data Properties
dateOfSignature = URIRef('http://www.w3.org/TR/2004/REC-xmlschema-2-20041028/dateOfSignature')
hasInscriptionContent = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasInscriptionContent')
hasSignature = URIRef('http://www.w3.org/TR/2004/REC-xmlschema-2-20041028/hasSignature')

baseUrl = Namespace("http://www.semanticweb.org/bianc/ontologies/2023/1/mat/resource/")

directory = 'data'

knowledgeGraph = Graph()

knowledgeGraph.bind("mat", baseUrl)

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if "paintings" in f:
        paintingsData = read_csv(f, sep=";",
                    keep_default_na=False,
                    )
    if "sculptures" in f: 
        sculpturesData = read_csv(f, sep=";",
            keep_default_na=False,
           )


for idx, row in paintingsData.iterrows():
    if row["Artwork component"] != '':
        id = URIRef(baseUrl + row["ID"])
        knowledgeGraph.add((id, RDF.type, ArtworkComponent))
    else: 
        id = URIRef(baseUrl + row["ID"])
        knowledgeGraph.add((id, RDF.type, Artwork))
    if row["Current support"] != '':
        knowledgeGraph.add((id, hasSupport, CurrentSupport))
        if row["Material"] != '':
            knowledgeGraph.add((CurrentSupport, isMadeOf, URIRef(baseUrl + "Support/" + row["Current support"])))
            knowledgeGraph.add((URIRef(baseUrl + "Support/" + row["Current support"]), RDF.type, Material))
            knowledgeGraph.add((URIRef(baseUrl + "Support/" + row["Current support"]), RDFS.Literal, Literal(row["Current support"])))
    if row["Original support"] != '':
        knowledgeGraph.add((CurrentSupport, transferredFrom, URIRef(baseUrl + "Support/" + row["Original support"])))
        knowledgeGraph.add((URIRef(baseUrl + "Support/" + row["Original support"]), RDF.type, OriginalSupport))
        knowledgeGraph.add((URIRef(baseUrl + "Support/" + row["Original support"]), isMadeOf, URIRef(baseUrl + "Material/" + row["Original support"])))
        knowledgeGraph.add((URIRef(baseUrl + "Material/" + row["Original support"]), RDF.type, Material))
        knowledgeGraph.add((URIRef(baseUrl + "Material/" + row["Original support"]), RDFS.Literal, Literal(row["Original support"])))
    if row["Decoration"] != '':
        knowledgeGraph.add((id, hasDecoration, URIRef(baseUrl + "Decoration/" + "decoration-" + row["ID"])))
        knowledgeGraph.add((URIRef(baseUrl + "Decoration/" +  "decoration-" + row["ID"]), RDF.type, Decoration))
        knowledgeGraph.add((URIRef(baseUrl + "Decoration/" +  "decoration-" + row["ID"]), RDFS.Literal, Literal(row["Decoration"])))
    if row["Ornament"] != '':
        knowledgeGraph.add((id, hasOrnament, URIRef(baseUrl + "Ornament/" + "ornament-" + row["ID"])))
        knowledgeGraph.add((URIRef(baseUrl + "Ornament/" +"ornament-" + row["ID"]), RDF.type, Ornament))
        knowledgeGraph.add((URIRef(baseUrl + "Ornament/" + "ornament-" + row["ID"]), RDFS.Literal, Literal(row["Ornament"])))
    if row["Signature"] != '':
        knowledgeGraph.add((id, hasSignature, URIRef(baseUrl + "Signature/" + "signature-" + row["ID"])))
        knowledgeGraph.add((URIRef(baseUrl + "Signature/" + "signature-" + row["ID"]), RDF.type, Signature))
        knowledgeGraph.add((URIRef(baseUrl + "Signature/" + "signature-" + row["ID"]), RDFS.Literal, Literal(row["Signature"])))
        if row["Signature datation"] != '':
            knowledgeGraph.add((Signature, isDated, URIRef(baseUrl + "SignatureDatation/" + "signatureDatation-" + row["ID"])))
            knowledgeGraph.add((URIRef(baseUrl + "SignatureDatation/" + "signatureDatation-" + row["ID"]), RDF.type, SignatureDatation ))
            knowledgeGraph.add((URIRef(baseUrl + "SignatureDatation/" + "signatureDatation-" + row["ID"]), RDFS.Literal, Literal(row["Signature datation"])))
    if row["Inscription"] != '':
        knowledgeGraph.add((id, hasInscription, URIRef(baseUrl + "Inscription/" + "inscription-" + row["ID"])))
        knowledgeGraph.add((URIRef(baseUrl + "Inscription/" + "inscription-" + row["ID"]), RDF.type, Inscription))
        knowledgeGraph.add((URIRef(baseUrl + "Inscription/" + "inscription-" + row["ID"]), RDFS.Literal, Literal(row["Inscription"])))
    if row["Technique"] != '':
        if "," in row["Technique"]:
            technique = str(row["Technique"]).split(",")
            for i in technique:
                i = i.replace(" ", "")
                knowledgeGraph.add((id, hasTechnique, URIRef(baseUrl + "Technique/" + i)))
                knowledgeGraph.add((URIRef(baseUrl + "Technique/" + i), RDF.type, Technique))
                knowledgeGraph.add((URIRef(baseUrl + "Technique/" + i), RDFS.Literal, Literal(i)))
                if row["Material"] != '':
                    knowledgeGraph.add((URIRef(baseUrl + "Technique/" + i), isPerformedOn, (URIRef(baseUrl + "Material/" + row["Material"]))))
                    knowledgeGraph.add((URIRef(baseUrl + "Material/" + row["Material"]), RDF.type, Material))
                    knowledgeGraph.add((URIRef(baseUrl + "Material/" + row["Material"]), RDFS.Literal, Literal(row["Material"])))
'''
venue_internal_id = {}
for idx, row in venues.iterrows():
    local_id = "venue-" + str(idx)
    
    # The shape of the new resources that are venues is
    # 'https://comp-data.github.io/res/venue-<integer>'
    subj = URIRef(base_url + local_id)
    
    # We put the new venue resources created here, to use them
    # when creating publications
    venue_internal_id[row["id"]] = subj
    
    if row["type"] == "journal":
        # RDF.type is the URIRef already provided by rdflib of the property 
        # 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
        my_graph.add((subj, RDF.type, Journal))
    else:
        my_graph.add((subj, RDF.type, Book))
    
    my_graph.add((subj, name, Literal(row["name"])))
    my_graph.add((subj, identifier, Literal(row["id"])))


endpoint = "http://192.168.1.2:9999/blazegraph/"

#https://github.com/comp-data/2021-2022/blob/main/docs/handson/05/05-Configuring_and_populating_a_graph_database.ipynb


g = Graph()



v = g.serialize(format="ttl")
'''
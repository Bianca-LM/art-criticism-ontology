from pandas import read_csv, Series
from rdflib import RDF, Graph, URIRef, RDFS, Literal, Namespace, serializer
import os


from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

#java -server -Xmx1g -jar blazegraph.jar
endpoint = "http://192.168.1.2:9999/blazegraph/sparql"

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
transferredFrom = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#transferredFrom')
isPerformedOn = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#isPerformedOn')
isSigned = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#isSigned')

#All the Data Properties
dateOfSignature = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#dateOfSignature')
hasInscriptionContent = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasInscriptionContent')
hasSignature = URIRef('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#hasSignature')

nameSpace = Namespace('http://www.semanticweb.org/bianc/ontologies/2023/1/mat#')

baseUrl = Namespace("http://www.semanticweb.org/bianc/ontologies/2023/1/mat/resource/")

directory = 'data'

knowledgeGraph = Graph()

knowledgeGraph.bind("mat", nameSpace)
knowledgeGraph.bind("mat-r", baseUrl)

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
        currentSupport = row["Current support"].replace(" ", "-")
        knowledgeGraph.add((id, hasSupport, CurrentSupport))
        knowledgeGraph.add((CurrentSupport, isMadeOf, URIRef(baseUrl + row["ID"] + "Support/" + currentSupport)))
        knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + currentSupport), RDF.type, CurrentSupport))
        knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + currentSupport), isMadeOf, URIRef(baseUrl + "Material/" + currentSupport)))
        knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + currentSupport), RDF.type, Material))
        knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + currentSupport), RDFS.Literal, Literal(row["Current support"])))
        if row["Original support"] != '':
            originalSupport = row["Original support"].replace(" ", "-")
            knowledgeGraph.add((CurrentSupport, transferredFrom, URIRef(baseUrl + row["ID"] + "Support/" + originalSupport)))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + originalSupport), RDF.type, OriginalSupport))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + originalSupport), isMadeOf, URIRef(baseUrl + "Material/" + originalSupport)))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + originalSupport), RDF.type, Material))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + originalSupport), RDFS.Literal, Literal(row["Original support"])))
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
                knowledgeGraph.add((id, hasTechnique, URIRef(baseUrl + row["ID"] + "Technique/" + i)))
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + i), RDF.type, Technique))
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + i), RDFS.Literal, Literal(i)))
                if row["Material"] != '':
                    material = row["Material"].replace(" ", "-")
                    knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + i), isPerformedOn, (URIRef(baseUrl + row["ID"] + "Material/" + material))))
                    knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + material), RDF.type, Material))
                    knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + material), RDFS.Literal, Literal(row["Material"])))
        else: 
            technique = row["Technique"].replace(" ", "-")
            knowledgeGraph.add((id, hasTechnique, URIRef(baseUrl + row["ID"] + "Technique/" + technique)))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + technique), RDF.type, Technique))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" +  technique), RDFS.Literal, Literal(technique)))
            if row["Material"] != '':
                material = row["Material"].replace(" ", "-")
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + technique), isPerformedOn, (URIRef(baseUrl + row["ID"] + "Material/" + material))))
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + material), RDF.type, Material))
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + material), RDFS.Literal, Literal(row["Material"])))


for idx, row in sculpturesData.iterrows():
    if row["Artwork component"] != '':
        id = URIRef(baseUrl + row["ID"])
        knowledgeGraph.add((id, RDF.type, ArtworkComponent))
    else: 
        id = URIRef(baseUrl + row["ID"])
        knowledgeGraph.add((id, RDF.type, Artwork))
    if row["Current support"] != '':
        currentSupport = row["Current support"].replace(" ", "-")
        knowledgeGraph.add((id, hasSupport, CurrentSupport))
        knowledgeGraph.add((CurrentSupport, isMadeOf, URIRef(baseUrl + row["ID"] + "Support/" + currentSupport)))
        knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + currentSupport), RDF.type, CurrentSupport))
        knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + currentSupport), isMadeOf, URIRef(baseUrl + "Material/" + currentSupport)))
        knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + currentSupport), RDF.type, Material))
        knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + currentSupport), RDFS.Literal, Literal(row["Current support"])))
        if row["Original support"] != '':
            originalSupport = row["Original support"].replace(" ", "-")
            knowledgeGraph.add((CurrentSupport, transferredFrom, URIRef(baseUrl + row["ID"] + "Support/" + originalSupport)))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + originalSupport), RDF.type, OriginalSupport))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Support/" + originalSupport), isMadeOf, URIRef(baseUrl + "Material/" + originalSupport)))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + originalSupport), RDF.type, Material))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + originalSupport), RDFS.Literal, Literal(row["Original support"])))
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
    if row["Carter's mark"] != '':
        knowledgeGraph.add((id, isMarked, URIRef(baseUrl + "Carter/" + "carter-" + row["ID"])))
        knowledgeGraph.add((URIRef(baseUrl + "Carter/" + "carter-" + row["ID"]), RDF.type, MarkOfCarter))
        knowledgeGraph.add((URIRef(baseUrl + "Carter/" + "carter-" + row["ID"]), RDFS.Literal, Literal(row["Carter's mark"])))
    if row["Founder's mark"] != '':
        knowledgeGraph.add((id, isMarked, URIRef(baseUrl + "Founder/" + "founder-" + row["ID"])))
        knowledgeGraph.add((URIRef(baseUrl + "Founder/" + "founder-" + row["ID"]), RDF.type, MarkOfFounder))
        knowledgeGraph.add((URIRef(baseUrl + "Founder/" + "founder-" + row["ID"]), RDFS.Literal, Literal(row["Founder's mark"])))
    if row["Inscription"] != '':
        knowledgeGraph.add((id, hasInscription, URIRef(baseUrl + "Inscription/" + "inscription-" + row["ID"])))
        knowledgeGraph.add((URIRef(baseUrl + "Inscription/" + "inscription-" + row["ID"]), RDF.type, Inscription))
        knowledgeGraph.add((URIRef(baseUrl + "Inscription/" + "inscription-" + row["ID"]), RDFS.Literal, Literal(row["Inscription"])))
    if row["Technique"] != '':
        if "," in row["Technique"]:
            technique = str(row["Technique"]).split(",")
            for i in technique:
                i = i.replace(" ", "")
                knowledgeGraph.add((id, hasTechnique, URIRef(baseUrl + row["ID"] + "Technique/" + i)))
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + i), RDF.type, Technique))
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + i), RDFS.Literal, Literal(i)))
                if row["Material"] != '':
                    material = row["Material"].replace(" ", "-")
                    knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + i), isPerformedOn, (URIRef(baseUrl + row["ID"] + "Material/" + material))))
                    knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + material), RDF.type, Material))
                    knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + material), RDFS.Literal, Literal(row["Material"])))
        else: 
            technique = row["Technique"].replace(" ", "-")
            knowledgeGraph.add((id, hasTechnique, URIRef(baseUrl + row["ID"] + "Technique/" + technique)))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + technique), RDF.type, Technique))
            knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" +  technique), RDFS.Literal, Literal(technique)))
            if row["Material"] != '':
                material = row["Material"].replace(" ", "-")
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Technique/" + technique), isPerformedOn, (URIRef(baseUrl + row["ID"] + "Material/" + material))))
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + material), RDF.type, Material))
                knowledgeGraph.add((URIRef(baseUrl + row["ID"] + "Material/" + material), RDFS.Literal, Literal(row["Material"])))
                
store = SPARQLUpdateStore()

store.open((endpoint, endpoint))

print(len(knowledgeGraph))


for triple in knowledgeGraph.triples((None, None, None)):
   print(triple)
   store.add(triple)
    
store.close()

ttl = knowledgeGraph.serialize(destination='knowledgeGraph.txt', format='turtle')

'''

endpoint = "http://192.168.1.2:9999/blazegraph/"

#https://github.com/comp-data/2021-2022/blob/main/docs/handson/05/05-Configuring_and_populating_a_graph_database.ipynb


g = Graph()



v = g.serialize(format="ttl")
'''
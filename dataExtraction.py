import os 
from pandas import *
import spacy
from collections import deque
import re
from deep_translator import GoogleTranslator
from sparql_dataframe import get
from SPARQLWrapper import *


#this function perform a sparql query on an endpoint and return it into JSON format
def askSkosVocabulary(endpoint, query):
    client = SPARQLWrapper(endpoint)
    client.setQuery(query)
    client.setReturnFormat(JSON)
    results = client.query().convert()
    finalResult = vocabularyTranslation(results)
    return finalResult

#automatic translation of the vocabulary from a JSON file returned by a SPARQL query
def vocabularyTranslation(jsonQueryResults): 
    data = set()
    enData = set()
    for i in jsonQueryResults["results"]["bindings"]:
        data.add(i["label"]["value"])
    for i in data: 
        enData.add(GoogleTranslator(source='it', target='en').translate(i))
    translatedData = correctTranslation(list(enData))
    return translatedData

#specific correction of the automatic tranlation
def correctTranslation(data):
    if "tin" in data: #this means it is the material vocabulary
        data.remove("tin") #tin and lands create ambiguation (since painting)
        data.remove("blue") 
        data.append("metal sheet") #for "latta"
    if "lands" in data: #this means is the technique vocabulary
        data.remove("lands")
        data.extend(["oil", "tempera"])
        data.append("earth") #for "terre"
    return data


#automatic extraction of data: it takes in input the directory of the .txt file where the information must be extracted and the two SKOS vocabulary
def dataExtraction(directory, materials, techniques):

    allExtractedData = {}

    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)

        nlp = spacy.load("en_core_web_lg")
        
        with open (file, "r", encoding="utf-8") as f:
            text = f.read()

        txt = []

        idx = 000 #the index we will give to each resource
        for paragraph in re.split(r'\n?\n\n\n', text):
            txt.append(paragraph)
            txt.append("PARAGRAPH END")
            #the first if finds a titles which contain the name of the artist
            if re.match(r'\n*[a-zA-Z ]+\n(?!\d)', paragraph): 
                processedParagraph = nlp(paragraph)
                if processedParagraph.ents[0].label_ == "PERSON" and processedParagraph.ents[0].text != False:
                    author = processedParagraph.ents[0].text  
                    if '\n' in author: 
                        author = re.sub(r'\n.+', '', author)
                        author = re.sub(r'\n', '', author) 
                    authorName = author
            #this if finds the titles which contain name of workshop of artists
            elif re.search(r'\n*Workshop of [a-zA-Z ]+(?!\d)', paragraph):
                workshopOfAuthor = "Workshop of "+authorName
                author = workshopOfAuthor
            
            elif re.match(r"\n*.+\n\d+", paragraph):
                #this block finds the titles which contains the name of the artwork and assign it to the artist
                title = re.search("\n*.+\n", paragraph).group() 
                if '\n' in title: 
                    title = re.sub(r'\n', '', title)
                if 'P'+str("{:03d}".format(idx)) not in allExtractedData:
                    allExtractedData["P"+str("{:03d}".format(idx))] = {"author": author, "title": title}
                else: 
                    allExtractedData["P"+str("{:03d}".format(idx))] = {"author": author, "title": title}
                
                #automatic extraction of materials from the paragraph
                usedMaterials = []
                for material in materials: 
                    findMaterial = re.findall(r'(?<![a-zA-Z])'+material+r'(?![a-zA-Z])', paragraph, flags=re.IGNORECASE)
                    usedMaterials.extend(findMaterial)
                allExtractedData["P"+str("{:03d}".format(idx))]["material"] = list(set(usedMaterials))
                
                #automatic extraction of techniques from the paragraph
                usedTechniques = []
                for technique in techniques: 
                    findTechniques = re.findall(r'(?<![a-zA-Z])'+technique+r'(?![a-zA-Z])', paragraph, flags=re.IGNORECASE)
                    usedTechniques.extend(findTechniques)
                allExtractedData["P"+str("{:03d}".format(idx))]["technique"] = list(set(usedTechniques))

                idx+=1

    #from JSON to CSV format          
    identifier = []
    author = []
    title = []
    material = []
    technique = []

    for key, value in allExtractedData.items(): 
        identifier.append(key)
        author.append(value["author"])
        title.append(value["title"])
        material.append(value["material"])
        technique.append(value["technique"])

    dataFrame = DataFrame({"identifier": Series(identifier, dtype=str), "author": Series(author, dtype=str), "title":Series(title, dtype=str), "material": Series(material), "technique":Series(technique)})

    dataFrame.to_csv("data/data.csv")



#endpoint where to perform the sparql queries to ask for the vocabularies
endpoint = 'https://dati.cultura.gov.it/sparql'

queryMaterials = """
SELECT DISTINCT ?material ?label WHERE {
    <http://dati.beniculturali.it/vocabularies/opere_e_oggetti_d_arte_materia/def/> skos:hasTopConcept ?material.
    ?material rdfs:label ?label
}
"""
queryTechniques = """
SELECT DISTINCT ?technique ?label WHERE {
    <http://dati.beniculturali.it/vocabularies/opere_e_oggetti_d_arte_tecnica/def/> skos:hasTopConcept ?technique.
    ?technique rdfs:label ?label.
}
"""

materials = askSkosVocabulary(endpoint, queryMaterials)

techniques = askSkosVocabulary(endpoint, queryTechniques)

dataExtraction("data/books", materials, techniques)
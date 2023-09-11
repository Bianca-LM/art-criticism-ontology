import os 
from pandas import *
import spacy
from collections import deque
import re
import json
from deep_translator import GoogleTranslator


def vocabulary(jsonPath): 
    data = set()
    enData = set()
    with open(jsonPath, "r", encoding="utf-8") as jsonFile: 
        vocabulary = json.load(jsonFile)
    for i in vocabulary["results"]["bindings"]:
        data.add(i["label"]["value"])
        print(data)
    for i in data: 
        enData.add(GoogleTranslator(source='it', target='en').translate(i))
        #elif GoogleTranslator(source='auto', target='en').translate(i["label2"]["value"]) not in data:
            #data.append(GoogleTranslator(source='auto', target='en').translate(i["label2"]["value"]))
    #translatedMaterials = GoogleTranslator(source='auto', target='it').translate_batch(data)
    return list(enData)

def textProcessing(directory):

    csv = {}

    
    materials = vocabulary("data/jsonMaterials.json")
    materials.remove("tin") #tin and lands create ambiguation (since painting)
    materials.remove("blue") #no clue why it is on the list, thanks to Google translator
    materials.append("metal sheet") #for "latta"
    techniques = vocabulary("data/jsonTechniques.json")
    techniques.remove("lands")
    techniques.extend(["oil", "tempera"])
    techniques.append("earth") #for "terre"

    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)

        nlp = spacy.load("en_core_web_lg")
        #Sample text
        with open (file, "r", encoding="utf-8") as f:
            text = f.read()

        #artistsDescription = re.findall(r"\n+\n+\(?!\d).+\n\(?!\d).*[.\n]*[.\n]*")
        #artworksParagraph = re.findall(r"\n+.+\n\d+\n?.*\n?.*\n?.*\n?.*")
        
        #paragraphs = re.findall(r'\n+.+\s?\n(?=[0-9]+).+\s?\n.*\s?\n?.*\s?\n?.*\s?\n?.*\s|.*\s?\n?.*\s?\n?.*\s?\n?.*\s?\n?.*', text)
        txt = []
        #paragraphs = re.findall("\\n+.+\\n\\d*.*\\n?.*\\n?.*\\n?.*", text)
        #paragraph = re.split("\\n.+\\n\\d+", text) 

        idx = 000
        for paragraph in re.split(r'\n?\n\n\n', text):
            txt.append(paragraph)
            txt.append("PARAGRAPH END")
            #print("AAAAAAAA", paragraph)
            if re.match(r'\n*[a-zA-Z ]+\n(?!\d)', paragraph): 
                processedParagraph = nlp(paragraph)
                if processedParagraph.ents[0].label_ == "PERSON" and processedParagraph.ents[0].text != False:
                    author = processedParagraph.ents[0].text  
                    if '\n' in author: 
                        author = re.sub(r'\n.+', '', author)
                        author = re.sub(r'\n', '', author) 
                    authorName = author
                    csv[author] = {}
            elif re.search(r'\n*Workshop of [a-zA-Z ]+(?!\d)', paragraph):
                workshopOfAuthor = "Workshop of "+authorName
                csv[workshopOfAuthor] = {} 
                author = workshopOfAuthor
            elif re.match(r"\n*.+\n\d+", paragraph):
                #= nlp(paragraph)
                title = re.search("\n*.+\n", paragraph).group()
                #paragraph = paragraph.replace("\n", " ") 
                if '\n' in title: 
                    title = re.sub(r'\n', '', title)
                if 'P'+str("{:03d}".format(idx)) not in csv:
                    csv[author]["P"+str("{:03d}".format(idx))] = {title: []}
                else: 
                    csv[author]["P"+str("{:03d}".format(idx))].update({title: []})

                #usedMaterials = set([word for word in materials if r" "+word in paragraph])
                #we take the last word found since the last sentence is the one containing technical information
                #for other books, just make sure that the variable paragraph coincides with the sentence containing technical information
                usedMaterials = []
                for material in materials: 
                    findMaterial = re.findall(r'(?<![a-zA-Z])'+material+r'(?![a-zA-Z])', paragraph, flags=re.IGNORECASE)
                    usedMaterials.extend(findMaterial)
                csv[author]["P"+str("{:03d}".format(idx))]["material"] = list(set(usedMaterials))
                #csv[author]["P"+str("{:03d}".format(idx))]["material"] = list(usedMaterials)
                
                #the word must be preceded by a space or a new line in order to avoid errors (as "tin" in "painting")
                usedTechniques = []
                for technique in techniques: 
                    findTechniques = re.findall(r'(?<![a-zA-Z])'+technique+r'(?![a-zA-Z])', paragraph, flags=re.IGNORECASE)
                    usedTechniques.extend(findTechniques)
                csv[author]["P"+str("{:03d}".format(idx))]["technique"] = list(set(usedTechniques))
                #usedTechniques = set([word for word in techniques if r" "+word in paragraph])
                #csv[author]["P"+str("{:03d}".format(idx))]["techniques"] = list(usedTechniques)
                idx+=1
                
                #csv[author]["artwork"] = title
                    #elif ent.label_
                #print(csv)
                '''        
                author = re.match(r'\n+.+\n(?!\d)', paragraph)
                print(author)
                csv[author] = []


        print(csv)


        nlpText = nlp(paragraph)
        
        entities = deque()
        
        for ent in nlpText.ents:
            print(ent.text, ent.label_)
        '''
    with open("data/data.json", "w", encoding="utf-8") as file:
        json.dump(csv, file, indent=4, ensure_ascii=False)

    with open("data/data.txt", "w", encoding="utf-8") as file:
        txt = ' '.join(txt)
        file.write(txt)

textProcessing("data/books")



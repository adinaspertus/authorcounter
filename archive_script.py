#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 15:34:05 2020

@author: adina
"""

# original inport method
# makes a list of dictionaries (each article is a dictionary)
import json

f = open("data/arxiv-metadata-oai-snapshot.json")

counter = 0
papers = []
for item in f:
    if counter < 100:
        item = json.loads(item)
#        print(item["authors"]) # comment out when you don't wnat a list of authors
        entry = {"doi":item["doi"], 
                 "title":item["title"],
                 "authors":item["authors"],
                 "year":item["journal-ref"], # need to pull last four digits 
                 "abstract":item["abstract"],
                 }
        papers.append(entry) #papers is a list of dictionaries
        counter += 1
    else:
        break
        
f.close()


# change no. to call different papers
papers[1]["abstract"] #we'll need to clean out the \n
papers[1]["title"]
papers[1]["authors"]
#papers[1]["year"]

#see whole entry
papers[2]
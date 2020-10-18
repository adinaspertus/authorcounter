#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 10:14:51 2020

@author: adina
"""


import json
#import os
#print(os.getcwd())

f = open("data/arxiv-metadata-oai-snapshot.json")

counter = 0
papers = []
for item in f:
    if counter < 100:
        item = json.loads(item)
        entry = {"doi":item["doi"], 
                 "title":item["title"],
                 "authors":item["authors"],
                 #"year":item[...], # need to pull this from ___
                 "abstract":item["abstract"],
                 }
        papers.append(entry)
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



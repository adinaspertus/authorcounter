#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 10:14:51 2020

@author: adina
"""
#https://www.kaggle.com/Cornell-University/arxiv
#https://arxiv.org/help/api/user-manual#python_simple_example


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

# develop a program in a different file for counting authors
# ignore anything in a parentheses
# find all ", and" and replace with an *
# spit is either ", " "and" or "*"        
        


# change no. to call different papers

papers[1]["abstract"] #we'll need to clean out the \n
papers[1]["title"]
papers[1]["authors"]
#papers[1]["year"]

#see whole entry
papers[2]


for i in papers:
    print(papers[i]["authors"])

#print(papers[]["authors"])

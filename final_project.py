#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 10:14:51 2020

@author: adina
"""
#https://www.kaggle.com/Cornell-University/arxiv
#https://arxiv.org/help/api/user-manual#python_simple_example


import json
import pandas as pd


#pre-processing of the data
f = open("data/arxiv-metadata-oai-snapshot.json")

data  = []
counter = 0
with open("data/arxiv-metadata-oai-snapshot.json", "r") as f:
    for line in f: 
        if counter < 100:
            data.append(json.loads(line))
            counter += 1
f.close()


dict_ = {"doi": [], "title": [], "authors": [], "date": [], "abstract": []}
for paper in data:
    dict_["doi"].append(paper["doi"]),
    print(dict_["doi"]),
    dict_["title"].append(paper["title"]),
    print(dict_["title"])
    dict_["authors"].append(paper["authors"]),
    dict_["date"].append(paper["update_date"]),
    dict_["abstract"].append(paper["abstract"])

df = pd.DataFrame(dict_, columns=["doi", "title", "authors", "date", "abstract"])
df.head(5)
df.info()






for i in papers:
    print(papers[i]["authors"])

#print(papers[]["authors"])

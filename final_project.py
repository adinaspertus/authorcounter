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
#import name_counter as nc
import re

# define name counter program (move to new script later?)
# Comment any edits to the name_counter program

def name_counter(n):
    #import re

    # while loop to remove 
    while "(" in n:
        par = re.search('\(([^)]+)', n).group(1) # find text in parenthesis
        n = n.replace("("+par+")", "") # remove anything in parentheticals
   
<<<<<<< HEAD
    # tag all the splitters with a $
=======
    # tag all the splitters with a $$
>>>>>>> b7a8fb88723eceaa524118c970eec14a3b42180d
    n = n.replace(", and", " $$") 
    n = n.replace("and", "$$")
    n = n.replace(",", "$$")
   
    # split into a list
    a = n.split("$$")
    return(len(a))
    

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


dict_ = {"doi": [], "title": [], "authors": [], "a_count": [], "date": [], "abstract": []}
for paper in data:
    dict_["doi"].append(paper["doi"]),
    dict_["title"].append(paper["title"]),
    dict_["authors"].append(paper["authors"]),
    dict_["a_count"].append(name_counter(paper["authors"])),
    dict_["date"].append(paper["update_date"]),
    dict_["abstract"].append(paper["abstract"])
#column names
df = pd.DataFrame(dict_, columns=["doi", "title", "authors", "a_count", "date", "abstract"])
df.head(5)
df.info()

print((name_counter("adina, ofer, hannah, and huey")))

# Create a copy of the DataFrame to work from
# Omit random state to have different random split each run
df_copy = df.copy()
train_set = df_copy.sample(frac=0.75, random_state=0)
test_set = df_copy.drop(train_set.index)


print(train_set)



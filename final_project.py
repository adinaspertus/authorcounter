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
import re #remove if we get name_counter to different script
import nltk

# define name counter program (move to new script later)
# NOTE: Please comment any edits to the name_counter program

def name_counter(n):
    #import re

    # while loop to remove 
    while "(" in n:
        par = re.search('\(([^)]+)', n).group(1) # find text in parenthesis
        n = n.replace("("+par+")", "") # remove anything in parentheticals
   
    # tag all the splitters with a $
    n = n.replace(", and", " $$") 
    n = n.replace("and", "$$")
    n = n.replace(",", "$$")
   
    # split into a list
    a = n.split("$$")
    return(len(a))
    
#see if name_counter is working (useful testing imported version of it)
print((name_counter("adina, ofer, hannah, and huey")))

#pre-processing of the data
#import subset of data from file
f = open("data/arxiv-metadata-oai-snapshot.json")
data  = []
counter = 0
with open("data/arxiv-metadata-oai-snapshot.json", "r") as f:
    for line in f: 
        if counter < 100:
            data.append(json.loads(line))
            counter += 1
f.close()

#create dictionary to convert into panda
dict_ = {"doi": [], "title": [], "authors": [], "a_count": [], "date": [], "abstract": []}
for paper in data:
    dict_["doi"].append(paper["doi"]),
    dict_["title"].append(paper["title"]),
    dict_["authors"].append(paper["authors"]),
    dict_["a_count"].append(name_counter(paper["authors"])),
    dict_["date"].append(paper["update_date"]),
    dict_["abstract"].append(paper["abstract"]),
    
#set panda column names
df = pd.DataFrame(dict_, columns=["doi", "title", "authors", "a_count", "date", "abstract"])
df.head(5)
df.info()

# we could define a function that does this called "clean" or something 
# and then import it in from a separate script

#convert abstract columns into lists of lowercase words
df["abstract"] = df["abstract"].str.lower()
#remove latex (anything within $...$)
df["abstract"] = df["abstract"].apply(lambda elem: re.sub(r"\$.+\$", "", elem))
#special characters (this line modified from: https://towardsdatascience.com/text-cleaning-methods-for-natural-language-processing-f2fc1796e8c7
df["abstract"] = df["abstract"].apply(lambda elem: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", " ", elem))  
#remove numbers
df["abstract"] = df["abstract"].apply(lambda elem: re.sub(r"\d+", "", elem))
#remove extra spaces (replace all space chunks with one space)
df["abstract"] = df["abstract"].apply(lambda elem: re.sub(r"[\s]+", " ", elem))

print(df["abstract"][2])



#split with a space
#we need to clean the abstract texts before this 
df["ab_split"] = list(df["abstract"].str.split(" "))
print(df["ab_split"])

              

# Create a copy of the DataFrame to work from
# Omit random state to have different random split each run
#df_copy = df.copy()
#create training data set
#at the moment it will not work because I first need to tokanize all the abstracts
#train_set = df_copy.sample(frac=0.75, random_state=0)
#train_set["x_train"] = train_set["abstract"]
#train_set["y_train"] = train_set["a_count"]

#create training data set
#test_set = df_copy.drop(train_set.index)
#test_set["X_test"] = test_set["abstract"]
#test_set["Y_test"]= test_set["a_count"]





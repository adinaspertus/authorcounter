#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 10:14:51 2020

@author: Adina Spertus-Melhus & Ofer Dotan

Note: Please download dataset from: https://www.kaggle.com/Cornell-University/arxiv
"""

######################################################

import json
import pandas as pd
import random
from collections import Counter
from functions import line_counter
from functions import name_counter 
from functions import year_extractor
from functions import text_cleaner
from functions import balance_test_set
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer #this can turn a corpus into a feature matrix

######################################################
# this section pre-processes the data


# determine subset of data to import file
nr_import = 1000 # choose how many abstracts to import (train set = 75%)

data_source_file = open("data/arxiv-metadata-oai-snapshot.json")

data  = []
with open("data/arxiv-metadata-oai-snapshot.json", "r") as data_source_file:
    total_lines = line_counter(data_source_file)

    # randomly generate list of indexes to get from database
    line_index = random.sample(range(total_lines), k=nr_import)

data_source_file.close()

# import pre-determined abstracts
with open("data/arxiv-metadata-oai-snapshot.json", "r") as data_source_file:
        
    while len(line_index)>0:      
        counter = 0
        for line in data_source_file:
            if counter in line_index: 
                data.append(json.loads(line))
                line_index.remove(counter)
            counter += 1
            
    # slower alternative to version above, but kept as another option if needed    
    # counter = 0       
    # for line in data_source_file:
    #     if counter in line_index:
    #         data.append(json.loads(line))
    #     counter += 1
                                   
data_source_file.close()

# create dictionary to convert into panda
# note: many of these variables are unused here, but could be useful for a further analysis
data_ = {
    "doi": [], 
    "title": [], 
    "authors": [], 
    "a_count": [], 
    "date": [],
    "year": [], 
    "abstract": []}

for paper in data:
    data_["doi"].append(paper["doi"]),
    data_["title"].append(paper["title"]),
    data_["authors"].append(paper["authors"]),
    data_["a_count"].append(name_counter(paper["authors"])), # applies name_counter fun
    data_["date"].append(paper["versions"][0]["created"]) 
    data_["year"].append(year_extractor(paper["versions"][0]["created"])) # applies year_extractor fun
    data_["abstract"].append(paper["abstract"]),
    
# set panda column names
data_pd = pd.DataFrame(
    data_, 
    columns=["doi", # will be removed
             "title", # will be removed
             "authors", # will be removed
             "a_count", 
             "date", # will be removed
             "year", 
             "abstract"]
    )

#run text cleaning function on abstract text
data_pd["abstract"] = text_cleaner(data_pd["abstract"])

# copy of the DataFrame to work from
data_pd_copy = data_pd.copy()

#keep only X, y1 (author count), and y2 (year)
data_pd_copy["X"] = data_pd_copy["abstract"] #X is list of abstracts
data_pd_copy["y1"] = data_pd_copy["a_count"] #y1 is list of number of authors
data_pd_copy["y2"] = data_pd_copy["year"] #y2 is year # consider in the future changing to decade
data_pd_copy.drop("doi", inplace=True, axis=1)
data_pd_copy.drop("title", inplace=True, axis=1)
data_pd_copy.drop("year", inplace=True, axis=1)
data_pd_copy.drop("authors", inplace=True, axis=1)
data_pd_copy.drop("abstract", inplace=True, axis=1)
data_pd_copy.drop("a_count", inplace=True, axis=1)
#data_pd_copy.info() # can be used to view dataframe info

#################################################################################
# this section initializes the (untrained) multinomial naive bayes classifier 

# training instance 1 (based on author count)
X1_train, X1_test, y1_train, y1_test = train_test_split(
    data_pd_copy.X, data_pd_copy.y1, test_size=0.25, random_state=0
    )

# training instance 2 (based on year) --> see below
X2_train, X2_test, y2_train, y2_test = train_test_split(
    data_pd_copy.X, data_pd_copy.y2, test_size=0.25, random_state=0
    )

# balance test sets to make all categories equally represented compared to rarest category
X1_test, y1_test = balance_test_set(X1_test, y1_test) # balance author number
X2_test, y2_test = balance_test_set(X2_test, y2_test, skip_y=[198]) # balance year, leave out 1980s

# create new Multinomial naive bayes classifier (untrained)
mnf1 = MultinomialNB(fit_prior=False) #telling it whether to generate prior probabilities
mnf2 = MultinomialNB(fit_prior=False)

vectorizer = CountVectorizer() #initialize a new vectorizer

#################################################################################
# this section fits and tests a predictor for author count

print("\n\nFitting and training AUTHOR NUMBER")
print("Training set distribution", Counter(y1_train))
print("Test set distribution", Counter(y1_test))

# turn list of abstracts into a vectorized feature matrix with 1 abstract per row
X1_train_vector = vectorizer.fit_transform(X1_train)
fitted_mnf1 = mnf1.fit(X1_train_vector.todense(), y1_train)
print("Fitted. Now will predict:")

# vectorize the text to be predicted
X1_test_vector = vectorizer.transform(X1_test)

prediction1 = fitted_mnf1.predict(X1_test_vector.todense())
print("Made prediction. Now testing prediction")

# report accuracy
correct_answers = 0
for guess, answer in zip(prediction1, y1_test):
    if guess == answer: # author counter
        correct_answers += 1
        
        
accuracy = 100*(correct_answers/len(y1_test))     
print("Accurate guesses:", accuracy, "%\n\n")

#################################################################################
# this section fits and tests a predictor for year

print("Fitting and training DECADE")
print("Training set distribution", Counter(y2_train))
print("Test set distribution", Counter(y2_test))

# turn list of abstracts into a vectorized feature matrix
X2_train_vector = vectorizer.fit_transform(X2_train)
fitted_mnf2 = mnf2.fit(
    X2_train_vector.todense(), 
    y2_train
    )

# vectorize the text to be predicted
X2_test_vector = vectorizer.transform(X2_test)

#X_test_vector = X_test_vector.todense()
prediction2 = fitted_mnf2.predict(
    X2_test_vector.todense()
    )
print("Made prediction. Now testing prediction")

# report accuracy for year test
# note: 3 year window option commented out because not appropriate for decades
# however could be useful for a future version that predicts single years
correct_answers = 0
for guess, answer in zip(prediction2, y2_test):
    # if (guess <= answer + 1) and (guess >= answer - 1): #3 year window
    #     print("guess:", guess, "year:", answer) 
    #     correct_answers += 1

    if guess == answer:
        correct_answers += 1

accuracy = 100*(correct_answers/len(y2_test))     
print("Accurate guesses:", accuracy, "%")

#################################################################################



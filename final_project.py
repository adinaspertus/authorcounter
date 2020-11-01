#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 10:14:51 2020

@author: adina and ofer
"""
#https://www.kaggle.com/Cornell-University/arxiv
#https://arxiv.org/help/api/user-manual#python_simple_example


#to do (no particular order): 
    #1. create mini json file for testing *** do before sunday
    #2. run the test on a randomized range of years so that it doesn't
    #just look at 2006-2009!
    #3. tkInter app
    #4. test on equal number of 1 author vs. multiple author papers
    
#also consider: 
    #TFIDF counts
    #testing decade instead of year
    #running on larger test dataset 
    #test SDGC classifier to see if more accurate (once better test data set up)
    
######################################################

import json
import pandas as pd
from functions import name_counter 
from functions import text_cleaner

    
#see if name_counter is working (or if it is testing true number or 1 vs. multiple)
print((name_counter("adina, ofer, hannah, and huey")))

######################################################
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
dict_ = {"doi": [], "title": [], "authors": [], "a_count": [], "year": [], "abstract": []}
for paper in data:
    dict_["doi"].append(paper["doi"]),
    dict_["title"].append(paper["title"]),
    dict_["authors"].append(paper["authors"]),
    dict_["a_count"].append(name_counter(paper["authors"])),
    dict_["year"].append(int(paper["update_date"][:4])), #only takes first 4 digits, ie year
    dict_["abstract"].append(paper["abstract"]),
    
#set panda column names
df = pd.DataFrame(dict_, columns=["doi", "title", "authors", "a_count", "year", "abstract"])
df.head(5)
df.info()

#run text cleaning function from functions script
df["abstract"] = text_cleaner(df["abstract"])
#see what output looks like (delete later)
print(df["abstract"][2])

#################################################################################
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB #CategoricalNB
#from  sklearn.linear_model import SGDClassifier #keep for now, may test this later
from sklearn.feature_extraction.text import CountVectorizer #this can turn a corpus into a feature matrix

# copy of the DataFrame to work from
df_copy = df.copy()

#keep only X, y1 (author count), and y2 (year)
df_copy.info()
df_copy["X"] = df_copy["abstract"] #X is list of abstracts
df_copy["y1"] = df_copy["a_count"] #y1 is list of number of authors
df_copy["y2"] = df_copy["year"] #y2 is year # consider in the future changing to decade
df_copy.drop("doi", inplace=True, axis=1)
df_copy.drop("title", inplace=True, axis=1)
df_copy.drop("year", inplace=True, axis=1)
df_copy.drop("authors", inplace=True, axis=1)
df_copy.drop("abstract", inplace=True, axis=1)
df_copy.drop("a_count", inplace=True, axis=1)
df_copy.info()

#training instance 1 (based on author count)
X1_train, X1_test, y1_train, y1_test = train_test_split(df_copy.X, df_copy.y1, test_size=0.25, random_state=0)

#training instance 2 (based on year) --> see below
X2_train, X2_test, y2_train, y2_test = train_test_split(df_copy.X, df_copy.y2, test_size=0.25, random_state=0)

#fit a new Multinomial naive bayes classifier
mnf1 = MultinomialNB()
mnf2 = MultinomialNB()
#sdg = SGDClassifier()
vectorizer = CountVectorizer() #initializing a new vectorizer

#################################################################################
# This section creates a predictor for author count

#turn list of abstracts into a vectorized feature matrix...
#...each row is 1 abstract
X1_train_vector = vectorizer.fit_transform(X1_train)
#MAYBE come back later to add TFIDF counts here
fitted_mnf1 = mnf1.fit(X1_train_vector.todense(), y1_train)
print("Fitted. Now will predict:")

#vectorize the text to be predicted
X1_test_vector = vectorizer.transform(X1_test)
#MAYBE also TFIDF here

#X_test_vector = X_test_vector.todense()
prediction1 = fitted_mnf1.predict(X1_test_vector.todense())
print("Made prediction. Now testing prediction")

#report accuracy
correct_answers = 0
for guess, answer in zip(prediction1, y1_test):
    if guess == answer: #author counter
        correct_answers += 1
        
        
accuracy = 100*(correct_answers/len(y1_test))     
print("Accurate guesses:", accuracy, "%")

#################################################################################
# This section creates a predictor for year

#turn list of abstracts into a vectorized feature matrix
X2_train_vector = vectorizer.fit_transform(X2_train)
#MAYBE come back later to add TFIDF counts here
fitted_mnf2 = mnf2.fit(X2_train_vector.todense(), y2_train)
print("Fitted 2. Now will predict 2:")

#vectorize the text to be predicted
X2_test_vector = vectorizer.transform(X2_test)
#MAYBE also TFIDF here

#X_test_vector = X_test_vector.todense()
prediction2 = fitted_mnf2.predict(X2_test_vector.todense())
print("Made prediction. Now testing prediction")

#report accuracy for year test
correct_answers = 0
for guess, answer in zip(prediction2, y2_test):
    if (guess <= answer + 1) and (guess >= answer - 1): #3 year window
        print("guess:", guess, "year:", answer) #problem: only looking at 2007-2009
        correct_answers += 1

accuracy = 100*(correct_answers/len(y2_test))     
print("Accurate guesses:", accuracy, "%")

#################################################################################

#define function to be used by TKinter
def predict_abstract(abstract):
    abstract = pd.Series(data=[abstract])
    abstract = text_cleaner(abstract)
    abstract_vector = vectorizer.transform(abstract) 
    #print(abstract_vector)
    prediction_author = fitted_mnf1.predict(abstract_vector.todense())[0] #returns first list item
    prediction_year = fitted_mnf2.predict(abstract_vector.todense())[0] #same as above
    return [prediction_author, prediction_year]


#test:    
#predict_abstract("ths is a l..df lije# {{ hi")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
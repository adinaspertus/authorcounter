#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 10:14:51 2020

@author: adina and ofer
"""
#https://www.kaggle.com/Cornell-University/arxiv
#https://arxiv.org/help/api/user-manual#python_simple_example


# to do list: 
    # create another function that runs with year 
    # (make accuracy based on a 3 window (one year more or less))


import json
import pandas as pd
#import name_counter as nc
import re #remove if we move name_counter and cleaning to diff script
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
    
    #returning int #changed 
    if len(a) == 1:
        return(len(a))
    else:
        return 2
    
    
#see if name_counter is working (useful testing imported version of it)
print((name_counter("adina, ofer, hannah, and huey")))

#pre-processing of the data
#import subset of data from file
f = open("data/arxiv-metadata-oai-snapshot.json")
data  = []
counter = 0
with open("data/arxiv-metadata-oai-snapshot.json", "r") as f:
    for line in f: 
        if counter < 1000:
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
#remove space at beginning of text
df["abstract"] = df["abstract"].apply(lambda elem: re.sub(r"\A[\s]", "", elem))
#remove space at lend of text
df["abstract"] = df["abstract"].apply(lambda elem: re.sub(r"\Z[\s]", "", elem))


#see what output looks like (delete later)
print(df["abstract"][2])


#split with a space
# df["ab_split"] = list(df["abstract"].str.split(" "))
# print(df["ab_split"])

              

# Create a copy of the DataFrame to work from
# Omit random state to have different random split each run
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB, MultinomialNB
#from  sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer #this can turn a corpus into a feature matrix

df_copy = df.copy()

##first trial = divide samples into train/test
#create training data set
#train_set = df_copy.sample(frac=0.75, random_state=0)
#train_set["x_train"] = train_set["abstract"]
#train_set["y_train"] = train_set["a_count"]

#create training data set
#test_set = df_copy.drop(train_set.index)
#test_set["X_test"] = test_set["abstract"]
#test_set["Y_test"]= test_set["a_count"]

#second trial = leave data only with X and y and then train/test split
df_copy.info()
df_copy["X"] = df_copy["abstract"] #X is list of words
df_copy["y"] = df_copy["a_count"] #y is number of authors
#df_copy["y"] = df_copy["date"] #y is date
df_copy.drop("doi", inplace=True, axis=1)
df_copy.drop("title", inplace=True, axis=1)
df_copy.drop("date", inplace=True, axis=1)
df_copy.drop("authors", inplace=True, axis=1)
df_copy.drop("abstract", inplace=True, axis=1)
df_copy.drop("a_count", inplace=True, axis=1)
df_copy.info()

#X is list of abstracts' contents and y is number of authors - put in sci-kit format? 
X_train, X_test, y_train, y_test = train_test_split(df_copy.X, df_copy.y, test_size=0.25, random_state=0)

#fit a new categorical naive bayes classifier
#clf = CategoricalNB() #this might not be appropriate
mnf = MultinomialNB()
#sdg = SGDClassifier()
vectorizer = CountVectorizer() #initializing a new vectorizer

#turn list of abstracts into a vectorized feature matrix...
#...each row is 1 abstract
X_train_vector = vectorizer.fit_transform(X_train)
#MAYBE come back later to add TFIDF counts here
fitted_mnf = mnf.fit(X_train_vector.todense(), y_train)
print("Fitted. Now will predict:")

#vectorize the text to be predicted
X_test_vector = vectorizer.transform(X_test)
#MAYBE also TFIDF here

#X_test_vector = X_test_vector.todense()
prediction = fitted_mnf.predict(X_test_vector.todense())
print("Made prediction. Now testing prediction")

#report accuracy
correct_answers = 0
for guess, answer in zip(prediction, y_test):
    if (guess <= answer) and (guess >= answer - 1): #3 year window
    #if guess == answer:
        correct_answers += 1
        
accuracy = 100*(correct_answers/len(y_test))     
print("Accurate guesses:", accuracy, "%")


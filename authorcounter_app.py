#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 20:42:24 2020

@author: adina and ofer
"""

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


#creating the app that would contain our project

from tkinter import *

#main screen of app
root = Tk()
#resizing the size of the app window
root.geometry("1000x1000+150+150")
root.iconbitmap("/Users/mac/Documents/University/Hertie/Courses/Year 2/Python/Final project/authorcounter")

#creating main label 
label = Label(root, text="Author Counter", fg="aquamarine4")
label.config(font=("Courier", 44))
label.grid(row=0, column=2, sticky=E+W)#pushing it onto the screen
#sub label
sub_label = Label(root, text="Discover how many authors wrote the text you are reading with", fg="aquamarine4")
sub_label.config(font=("Courier", 24))
sub_label.grid(row=1, column=2, sticky=E+W)#sticky aims to keep in same location but need to learn it better 

entry_label = Label(root, text = "Please insert text in the box below",fg="dark slate gray")
entry_label.config(font=("Courier", 18))
entry_label.grid(row=4, column=2, sticky=E+W)

#define a function what happens when clicking the button
#for colours check http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

#elements to later integrate in the main function
#1 create entrybox with a sting variable content
entry_text = StringVar() # the text in  your entry
entry_widget = Entry(root,  width = 100, bg="wheat2", fg="white", textvariable=entry_text) # the entry
entry_widget.grid(row=5, column=2, ipady=80, sticky=E+W)


#make entry input into text document
def text():
    def save():
        t= entry_text.get()
        with open((t + '.txt'), 'w') as text: 
            text.write(t)
            
##function that would go into the app later

def clickButton():
    X_test = vectorizer.transform(text())
    prediction = fitted_mnf.predict(X_test_vector.todense())
    correct_answers = 0
    for guess, answer in zip(prediction, y_test):
        if guess == answer:
            correct_answer+=1,
            print("The model predict the paper was written by a single author"),
        accuracy = 100*(correct_answers/len(y_test)),
        print("Accurate guesses:", accuracy, "%"),
    else:
        print("The model predict the paper was written by more than one author"),
        accuracy = 100*(correct_answers/len(y_test))
        print("Accurate guesses:", accuracy, "%")
        

#combine two functions into one
def text_clickButton():
    text()
    clickButton()
    

#create the button to attach to the entry box
button = Button(root, text="Predict Number of Authors", command=text) # to attach to entry box add command= function name
button.grid(row=6, column=2, sticky=E+W)


#to attach button to function use command= function_name)



##add picture 
from PIL import ImageTk, Image
image_sh = Image.open("Shakespeare.jpg")
image_sh = image_sh.resize((150,200), Image.ANTIALIAS)
image_sh = ImageTk.PhotoImage(image_sh)
image_label=(Label(image=image_sh))
image_label.grid(row= 0, column=4)



#main loop for the program to run until closed
root.mainloop()


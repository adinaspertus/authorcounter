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

#################################################################################
# Q for Ofer: Can we delete this section? 
#https://arxiv.org/help/api/user-manual#python_simple_example
##first trial = divide samples into train/test 
#create training data set
#train_set = df_copy.sample(frac=0.75, random_state=0)
#train_set["x_train"] = train_set["abstract"]
#train_set["y_train"] = train_set["a_count"]

#create training data set
#test_set = df_copy.drop(train_set.index)
#test_set["X_test"] = test_set["abstract"]
#test_set["Y_test"]= test_set["a_count"]



#attempt turn entry input into text document
def text():
    def save():
        t= entry_text.get()
        with open((t + '.txt'), 'w') as text: 
            text.write(t)
                  
##function that would go into the app later
def clickButton():
    X_test = vectorizer.transform(entry_widget.get())
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



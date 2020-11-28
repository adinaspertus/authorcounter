#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 13:56:34 2020

@author: adina
"""
# regrex code from: https://stackoverflow.com/questions/38999344/extract-string-within-parentheses-python


import re
from collections import Counter
#import json
#import pandas as pd


def line_counter(file):
    total_lines = 0
    for line in file: 
        total_lines += 1
    return total_lines




def name_counter(names):

    # while loop to remove 
    while "(" in names:
        par = re.search('\(([^)]+)', names).group(1) # find text in parenthesis
        names = names.replace("("+par+")", "") # remove anything in parentheticals
   
    # tag all the splitters with a $
    names = names.replace(", and", " $$") 
    names = names.replace("and", "$$")
    names = names.replace(",", "$$")
   
    # split into a list
    names_list = names.split("$$")
    
    # return actual number of authors
    # return(len(names_list))
    
    #returning either 1 or 2 (for multiple) author count
    if len(names_list) == 1:
        return(len(names_list))
    else:
        return 2

def year_extractor(date):
    year = re.search('(\d{4})', date)
    return int(year[0])

#test = "adina, and ofer (and a, b, c) and jj (d, e, and f)"
#print(name_counter(test))

#this only runs on panda series
def text_cleaner(column):
    #convert abstract columns into string of lowercase words
    column = column.str.lower()
    #remove latex (anything within $...$)
    column = column.apply(lambda elem: re.sub(r"\$.+\$", "", elem))
    #remove special characters (this line modified from: https://towardsdatascience.com/text-cleaning-methods-for-natural-language-processing-f2fc1796e8c7
    column = column.apply(lambda elem: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", " ", elem))  
    #remove numbers
    column = column.apply(lambda elem: re.sub(r"\d+", "", elem))
    #remove extra spaces (replace all space chunks with one space)
    column = column.apply(lambda elem: re.sub(r"[\s]+", " ", elem))
    #remove space at beginning of text
    column = column.apply(lambda elem: re.sub(r"\A[\s]", "", elem)) #combine with one below
    #remove space at lend of text
    column = column.apply(lambda elem: re.sub(r"\Z[\s]", "", elem))
    
    return column



def balance_test_set(X, y):
    """Reduce a test X and y set so that y categories are EQUALLY represented -- returns a tuple of X and y as lists
    so every category will only be in the list as often as the least common member
    Note: Retains elements in order they are listed in the original list, assuming they have already been randomized"""
    
    
    distribution = Counter(y) #create dictionary saying how many of each category is in test set
    categories = list(distribution.keys()) #list of categories
    print(categories)
    
    #get category with smallest number
    minimum = distribution[min(distribution)]
    
    newX, newY = [], [] #initialize a pair of blank lists
    
    new_counts = Counter() #new y category counter for balanced set
    
    for x_element, y_element in zip(X, y):
        if new_counts[y_element] < minimum: #if we haven't yet reached the desired number of elements in this category
        
            #add this pair of X and y to the new list
            newX.append(x_element)
            newY.append(y_element)
            
            #note that we have one more from this category
            new_counts[y_element] += 1 #note that the new
    
    print("New test set category distribution:", Counter(newY)) #make sure we reached the desired number of each category (equally balanced)
    
    return newX, newY
        
    
    
        
    


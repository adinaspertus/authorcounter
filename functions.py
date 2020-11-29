#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 13:56:34 2020

@author: adina & ofer
"""

import re
from collections import Counter

def line_counter(file):
    """Counts the number of lines of an opened, but unimported, dataset"""
    total_lines = 0
    for line in file: 
        total_lines += 1
    return total_lines


def name_counter(names):
    """Takes a list of author names and cleans based on various formats in 
    arXiv in order to identify the total number of authors."""
    
    # while loop to remove institution name from parenthesis
    while "(" in names:
        par = re.search('\(([^)]+)', names).group(1) # find text in parenthesis
        names = names.replace("("+par+")", "") # remove anything in parentheticals
   
    # tag all the name splitters with a $$
    names = names.replace(", and", " $$") 
    names = names.replace("and", "$$")
    names = names.replace(",", "$$")
   
    # split into a list based on $$ tag
    names_list = names.split("$$")
    
    # return actual number of authors # could be useful in a future model
    # return(len(names_list))
    
    #returning either 1 or 2 (ie multiple) author count
    if len(names_list) == 1:
        return(len(names_list)) # single author
    else:
        return 2 # multiple authors


def year_extractor(date):
    """Uses regex to identify the authoriship year from the publication date
    string. Then simplifies to first 3 digits to give the decade."""
    year = re.search('(\d{4})', date)
    year = year[0][:3] #remove [:3] to keep whole year, otherwise gets decade
    return int(year)


# this only runs on panda series
def text_cleaner(column):
    """Cleans new text inserted to the prediction model. 
    Returns a string of lower case words with no latex, special charactes, numbers, and redundant spaces"""
    #convert abstract columns into string of lowercase words
    column = column.str.lower()
    #remove latex (anything within $...$)
    column = column.apply(lambda elem: re.sub(r"\$.+\$", "", elem))
    #remove special characters (regex modified from: https://towardsdatascience.com/text-cleaning-methods-for-natural-language-processing-f2fc1796e8c7
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



def balance_test_set(X, y, skip_y = []):
    """Restricts a test X and y set so that y categories (ie author count, or decade) 
    are equally represented in order to accurately test predictive accuracy.
    Returns a tuple of X and y as lists so that each category will only be represented as often as the least common member.
    Note: Retains elements in order they are listed in the original list, assuming they have already been randomized.
    Note: For DECADE, only retains 1990s, 2000s, 2010s, 2020s to exclude possibility of one 1989 article limiting test set size."""
    
    distribution = Counter(y) # create dictionary saying how many of each category is in test set    
    minimum = distribution[min(distribution)]  # find category with smallest size
    newX, newY = [], [] # initialize a pair of blank lists
    new_counts = Counter() # new y category counter for balanced set
    
    for x_element, y_element in zip(X, y):
        if new_counts[y_element] < minimum and y_element not in skip_y: # if we haven't reached the desired number of elements in this category
        
            # add this pair of X and y to the new list
            newX.append(x_element)
            newY.append(y_element)
            
            # note that we have one more from this category
            new_counts[y_element] += 1 #note that the new
    
    return newX, newY
        
    
    
def authorLabel(prediction):
    """Returns a different label depending on the prediction output. 
    Used in the "predict_abstract"" function in authourcounter_app"""
    
    if prediction == 1:
        answer = "The model predicts a single author wrote this paper"
    if prediction > 1:
        answer = "The model predicts multiple authors wrote this paper"
    return answer
        
    


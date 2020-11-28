#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 13:56:34 2020

@author: adina
"""
# regrex code from: https://stackoverflow.com/questions/38999344/extract-string-within-parentheses-python


import re
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
    return(len(names_list))
    
    #returning either 1 or 2 (for multiple) author count
    # if len(names_list) == 1:
    #     return(len(names_list))
    # else:
    #     return 2

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




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 13:56:34 2020

@author: adina
"""
# regrex code from: https://stackoverflow.com/questions/38999344/extract-string-within-parentheses-python


# at top of the final_project file: 
# import name_counter

import re

def name_counter(n):
    # while loop to remove 
    while "(" in n:
        par = re.search('\(([^)]+)', n).group(1) # find text in parenthesis
        n = n.replace("("+par+")", "") # remove anything in parentheticals
   
    # tag all the splitters with a $
    n = n.replace(", and", " $") 
    n = n.replace("and", "$")
    n = n.replace(",", "$")
   
    # split into a list
    a = n.split("$")
    return(len(a))
    


test = "adina, and ofer (and a, b, c) and jj (d, e, and f)"
print(name_counter(test))

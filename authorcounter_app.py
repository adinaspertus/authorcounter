#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 20:42:24 2020

@author: ofer & adina

"""

from tkinter import *
from PIL import ImageTk, Image
from final_project import *
from tkinter import scrolledtext
import textwrap
from PIL import ImageTk, Image
from functions import authorLabel 

######################################################

# main app window
window = Tk()
window.title("Welcome to the AuthorCounter App!")

window.configure(bg = "light blue")

# resizing the size of the app window
window.geometry("1070x900+150+150")

window.iconbitmap(
    "https://github.com/adinaspertus/authorcounter/Shakespeare.jpg"
    )

# main label 
label = Label(
    window, 
    text="Author Counter", 
    fg="aquamarine4", 
    bg = "light blue"
    )

label.config(
    font=("Courier", 44)
    )

label.grid(
    row=0, 
    column=2
    )

# introduction label
sub_label = Label(
    window, 
    text="Let the classifier predict who wrote your text, and when...", 
    fg="aquamarine4", 
    bg = "light blue")

sub_label.config(
    font=("Courier", 24)
    )

sub_label.grid(
    row=1, 
    column=2)

# insert text label
entry_label = Label(
    window, 
    text = "Please insert text in the box below",
    fg="dark slate gray", 
    bg = "light blue")

entry_label.config(
    font=("Courier", 18)
    )

entry_label.grid(
    row=4, 
    column=2
    )

######################################################

# answer labels
author_label = Label(
    window, 
    width=40
    )

author_label.grid(
    row=8, 
    column=2
    )

year_label = Label(
    window, 
    width=40
    )

year_label.grid(
    row=9, 
    column=2
    )

# entry text box 
text = Text(
    window, 
    height = 2
    )

text.grid(
    row=5, 
    column=2, 
    ipady=100
    )

# button to attach to the entry box
button = Button(
    window,
    bg = "light blue",
    fg="dark slate gray",
    text="Predict",
    command=lambda: predict_abstract(
        abstract=text.get("1.0", END)
    )
)

button.grid(
    row=6, 
    column=2
    )

# add Shakespeare picture 
image_sh = Image.open("Shakespeare.jpg")

image_sh = image_sh.resize(
    (150,200), 
    Image.ANTIALIAS
    )

image_sh = ImageTk.PhotoImage(image_sh)

image_label=(Label(
    image=image_sh)
    )
image_label.grid(
    row=0, 
    column=3
    )

#add rights reserved label
label_rights = Label(
    window, 
    text="Based on STEM article abstracts from 1990 to present\n\n© 2020. All rights reserved to Adina Spertus and Ofer Dotan.",
    bg = "light blue",
    fg="dark slate gray"
    )

label_rights.grid(
    row=14, 
    column=2
    )

#FUNCTION TO PREDICT ABSTRACT AND YEAR FROM ENTERED TEXT
    
def predict_abstract(abstract):
    """Takes a text from entry box, cleans it, turns it to vectorized feature matrix 
    and then fit and predicts if single or multiple authors and publication decade. 
    output prediction is then attached to labels packed to the TKinter window.
    """
    abstract = pd.Series(data=[abstract])
    abstract = text_cleaner(abstract)
    abstract_vector = vectorizer.transform(abstract) 
    prediction_author = fitted_mnf1.predict(abstract_vector.todense())[0] # returns first list item
    prediction_year = fitted_mnf2.predict(abstract_vector.todense())[0] # same as above

    global author_label, year_label
    author_label.configure(
        text=authorLabel(prediction_author)) # returns different label depending on prediciton
    year_label.configure(
        text="The predicted decade of publication is the {}".format(str(prediction_year)+"0s"))

# instantiate variables for prediction label
answer = "Enter Answer"
prediction = ""

######################################################

# main loop for the program to run until closed
window.mainloop()

   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
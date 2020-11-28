#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 20:42:24 2020

@author: adina and ofer


"""

from tkinter import *
from PIL import ImageTk, Image
from final_project import *
from tkinter import scrolledtext
import textwrap
from PIL import ImageTk, Image
######################################################

#main app window
window = Tk()
window.title("Welcome to the AuthorCounter App!")
window.configure(bg = "light blue")
#resizing the size of the app window
window.geometry("1070x900+150+150")
window.iconbitmap(
    "https://github.com/adinaspertus/authorcounter/Shakespeare.jpg")
#main label 
label = Label(
    window, 
    text="Author Counter", 
    fg="aquamarine4", 
    bg = "light blue"
    )
label.config(
    font=("Courier", 44)
    )
label.grid(row=0, column=2)

#sub label
sub_label = Label(
    window, 
    text="Discover how many authors wrote the text you are reading with", 
    fg="aquamarine4", 
    bg = "light blue")
sub_label.config(
    font=("Courier", 24)
    )
sub_label.grid(row=1, column=2)

#entry label
entry_label = Label(
    window, 
    text = "Please insert text in the box below",
    fg="dark slate gray", 
    bg = "light blue")
entry_label.config(
    font=("Courier", 18)
    )
entry_label.grid(row=4, column=2)

######################################################

#answer labels
author_label = Label(window, width=40)
author_label.grid(row=8, column=2)
year_label = Label(window, width=40)
year_label.grid(row=9, column=2)

#text box (formerly entry)
text = Text(window, height = 2)
text.grid(row=5, column=2, ipady=100)

#create the button to attach to the entry box
button = Button(
    window,
    bg = "light blue",
    fg="dark slate gray",
    text="Predict",
    command=lambda: predict_abstract(
        abstract=text.get("1.0", END)
    )
)
button.grid(row=6, column=2)

#add picture 
image_sh = Image.open(
    "Shakespeare.jpg"
    )
image_sh = image_sh.resize(
    (150,200), 
    Image.ANTIALIAS
    )
image_sh = ImageTk.PhotoImage(image_sh)
image_label=(Label(
    image=image_sh)
    )
image_label.grid(row=0, column=3)

#add rights
label_rights = Label(window, 
                     text="© 2020. All rights reserved to Adina Spertus and Ofer Dotan.",
                     bg = "light blue",
                     fg="dark slate gray")
label_rights.grid(row=14, column=2)

#FUNCTION TO PREDICT ABSTRACT AND YEAR FROM ENTERED TEXT
    
def predict_abstract(abstract):
    abstract = pd.Series(data=[abstract])
    abstract = text_cleaner(abstract)
    abstract_vector = vectorizer.transform(abstract) 
    #print(abstract_vector)
    prediction_author = fitted_mnf1.predict(abstract_vector.todense())[0] #returns first list item
    prediction_year = fitted_mnf2.predict(abstract_vector.todense())[0] #same as above

    global author_label, year_label
    author_label.configure(
        text=authorLabel(prediction_author))
    year_label.configure(
        text="The predicted year of publication is {}".format(prediction_year))

#trial to make conditional label
#initiate variables
answer = "Enter Answer"
prediction = ""
#label function
def authorLabel(prediction):
    if prediction == 1:
        answer = "The model predicts a single author wrote this paper"
    if prediction > 1:
        answer = "The model predicts multiple authors wrote this paper"
    return answer


######################################################
#main loop for the program to run until closed
window.mainloop()

   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
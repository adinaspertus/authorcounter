#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 20:42:24 2020

@author: adina and ofer
"""

from tkinter import *
from PIL import ImageTk, Image
from final_project import predict_abstract

######################################################

#main app window
root = Tk()
root.title("Welcome to the AuthorCounter App!")
root.configure(bg = "light blue")
#resizing the size of the app window
root.geometry("1070x900+150+150")
root.iconbitmap("/Users/mac/Documents/University/Hertie/Courses/Year 2/Python/Final project/authorcounter")

#main label 
label = Label(root, text="Author Counter", fg="aquamarine4", bg = "light blue")
label.config(font=("Courier", 44))
label.grid(row=0, column=2)

#sub label
sub_label = Label(root, text="Discover how many authors wrote the text you are reading with", fg="aquamarine4", bg = "light blue")
sub_label.config(font=("Courier", 24))
sub_label.grid(row=1, column=2)

#entry label
entry_label = Label(root, text = "Please insert text in the box below",fg="dark slate gray", bg = "light blue")
entry_label.config(font=("Courier", 18))
entry_label.grid(row=4, column=2)


######################################################

#define function to be used by TKinter
author_label = Label(root, width=40)
author_label.grid(row=8, column=2)
year_label = Label(root, width=40)
year_label.grid(row=9, column=2)

#entry box
text = StringVar() # the text in  your entry
text_entry = Entry(root,  width = 100, bg="wheat2", fg="white", textvariable=text) 
text_entry.grid(row=5, column=2, ipady=100)

   
#create the button to attach to the entry box
#button = Button(root, text="Predict Number of Authors", command=predict_abstract)
#button = Button(root, text="Predict Number of Authors", command=lambda: predict_abstract(text_entry.get()))
button = Button(
    root,
    text="Predict",
    command=lambda: predict_abstract(
        abstract=text_entry.get()
    )
)
button.grid(row=6, column=2, sticky=W)

######################################################

#add picture 
image_sh = Image.open("Shakespeare.jpg")
image_sh = image_sh.resize((150,200), Image.ANTIALIAS)
image_sh = ImageTk.PhotoImage(image_sh)
image_label=(Label(image=image_sh))
image_label.grid(row=0, column=3)


######################################################
#main loop for the program to run until closed
root.mainloop()

   
    
    
    
    
    
    
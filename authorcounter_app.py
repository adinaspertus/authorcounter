#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 20:42:24 2020

@author: mac
"""

#creating the app that would contain our project

from tkinter import *

#main screen of app
root = Tk()
#resizing the size of the app window
root.geometry("1000x1000+150+150")


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

#elements for the function
#1 create entrybox with a sting variable content
entry_text = StringVar() # the text in  your entry
entry_widget = Entry(root,  width = 100, bg="wheat2", fg="white", textvariable = entry_text) # the entry
entry_widget.grid(row=5, column=2, ipady=80, sticky=E+W)



#create entrybox

#create the button to attach to the entry box
button = Button(root, text="Submit text") # to attach to entry box add command= function name
button.grid(row=6, column=2, sticky=E+W)


#to attach button to function use command= function_name)




#main loop for the program to run until closed
root.mainloop()
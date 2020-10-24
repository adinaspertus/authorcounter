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
label = Label(root, text="Author Counter")
#pushing it onto the screen
label.pack() #to manually set the label place use label.grid(row=, column=)

#main space within root
main = Canvas(root) 
main_panel = Canvas()
main.pack()



#define a function what happens when clicking the button
#elements for the function
#1 create entrybox with a sting variable content
entry_text = StringVar() # the text in  your entry
entry_widget = Entry(main, width = 20, textvariable = entry_text) # the entry
main.create_window(50, 50, window = entry_widget)

#create entrybox

#create the button to attach to the entry box
button = Button(root, text="Submit text") # to attach to entry box add command= function name
button.pack()


#to attach button to function use command= function_name)





#main loop for the program to run until closed
root.mainloop()

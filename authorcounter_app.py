#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 20:42:24 2020

@author: adina and ofer
"""

#creating the app that would contain our project
from tkinter import *

#main screen of app
root = Tk()
#resizing the size of the app window

root.geometry("1000x1000+150+150")
root.iconbitmap("/Users/mac/Documents/University/Hertie/Courses/Year 2/Python/Final project/authorcounter")

#creating main label 
label = Label(root, text="Author Counter", fg="aquamarine4")
label.config(font=("Courier", 44))
label.grid(row=0, column=2)

#sub label
sub_label = Label(root, text="Discover how many authors wrote the text you are reading with", fg="aquamarine4")
sub_label.config(font=("Courier", 24))
sub_label.grid(row=1, column=2)

#entry label
entry_label = Label(root, text = "Please insert text in the box below",fg="dark slate gray")
entry_label.config(font=("Courier", 18))
entry_label.grid(row=4, column=2)

#entry box
entry_text = StringVar() # the text in  your entry
entry_widget = Entry(root,  width = 100, bg="wheat2", fg="white", textvariable=entry_text) # the entry
entry_widget.grid(row=5, column=2, ipady=80)

#turn entry input into text document
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
        

#combine two functions into one
def main():
    text()
    clickButton()

#function for now - remove later  
def Click():
    guess = Label(root, text="This paper has so and so authors")
    guess.grid(row=7, column = 2)

#create the button to attach to the entry box
button = Button(root, text="Predict Number of Authors", command=Click) # to attach to entry box add command= function name
button.grid(row=6, column=2)

#funciton for now - remove later
def Click1():
    guess1=Label(root, text="This paper is from year")
    guess1.grid(row=7, column = 2)
#second button 
button1 = Button(root, text= "Predict year of publication", command=Click1)
button1.grid(row=6, column=3, padx=2)


##add picture 
from PIL import ImageTk, Image
image_sh = Image.open("Shakespeare.jpg")
image_sh = image_sh.resize((150,200), Image.ANTIALIAS)
image_sh = ImageTk.PhotoImage(image_sh)
image_label=(Label(image=image_sh))
image_label.grid(row=0, column=3, padx=5)


#main loop for the program to run until closed
root.mainloop()


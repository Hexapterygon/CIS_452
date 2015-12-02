#!/usr/bin/env python

from Tkinter import*
import tkMessageBox

root = Tk()

tkMessageBox.showinfo("Window Title", "Monkeys can live up to 300 years.")

answer = tkMessageBox.askquestion('Question 1', 'Do you like silly faces?')

if answer == 'yes':
    print('congrats')

root.mainloop()

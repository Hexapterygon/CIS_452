#!/usr/bin/env python

from Tkinter import*

root = Tk()

photo = PhotoImage(file="filepath")
label = Label(root, image = photo)
label.pack()



root.mainloop()

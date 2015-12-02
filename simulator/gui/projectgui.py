#!/usr/bin/env python 
"""GUI for Operating System Loader Simulation"""

from Tkinter import* 
import ScrolledText as tkst
import tkFileDialog as tfd
import tkMessageBox

__author__ = "Nathan Anderle"
__version__ = "1.0"
__email__ = "anderlna@mail.gvsu.edu"


class MainFrame(object):
    """The primary GUI element"""

    def __init__(self, numFrames, master):
       """TO DO"""

       self.filename = None
       self.curLine = 1.0
       self.totLine = 0

       self.textFrame = Frame(master, width = 300, height = 400, bg='white')
       self.textFrame.grid(column=0, padx=20)

       self.spacerFrame = Frame(master, width = 50)
       self.spacerFrame.grid(row=0, column = 1)

       self.fieldFrame = Frame(master)
       self.fieldFrame.grid(row=0, column=2, padx=20, pady=10)
       self.labelFont = ('times', 20)

       self.pTables = []
       self.pbFrame = Frame(master, width=500, height=200, borderwidth = 3, relief=SUNKEN)
       self.pbFrame.grid(row=2, column=0, sticky=S, columnspan=3)
       self.pLabel = Label(self.pbFrame, text="Page Tables")
       #self.pLabel.grid(row=0, column=0, sticky=W)
       self.rw = 0
       self.clm = 0

       for i in range(32):
           self.pTables.append(Button(self.pbFrame, height=1, width=8, text="Process "+ str(i), state=DISABLED))

           self.pTables[i].grid(row=self.rw, column=self.clm, sticky=W, padx=10)

           if self.clm <= 2:
               self.clm += 1
           else:
               self.rw += 1
               self.clm = 0

       self.bFrame = Frame(master, width=500, height=10)
       self.bFrame.grid(row=3, column=0, sticky=S, columnspan=3, pady=20)

       self.loadButton = Button(self.bFrame, text="load", command = self.showTrace)
       self.stepButton = Button(self.bFrame, text="step", state=DISABLED, command = self.highlight)

       self.fLabels =[]
       self.entLabels = []
       self.loadButton.grid(row=0, column=0, sticky=E)
       self.stepButton.grid(row=0, column=1, sticky=E)
      

       self.tracetape = tkst.ScrolledText(self.textFrame, width = 30, height = 20, bg='white', borderwidth = 3, relief=GROOVE, state=DISABLED)
       self.tracetape.grid()
       
       for i in range(numFrames):
           self.entLabels.append(Label(self.fieldFrame, text="P1 Text Page 8", bg="white", fg="red", relief=GROOVE, padx=10, pady=6,  font=self.labelFont))
           self.fLabels.append(Label(self.fieldFrame, text = "Frame " + str(i), padx=5,  font=self.labelFont))
           self.fLabels[i].grid(row=i, column=0, sticky=W)
           self.entLabels[i].grid(row=i, column=1, sticky=E, columnspan=2)


    def showTrace(self):
        """TO DO"""
        self.filename= tfd.askopenfilename()
        if self.filename != '':
            if self.filename.endswith('.data'):
                self.totLine = 0
                self.curLine = 1.0
                self.stepButton.config(state=NORMAL)
                self.tracetape.config(state=NORMAL)
                self.tracetape.delete(1.0, END)
                f = open(self.filename)
                for line in f:
                    self.tracetape.insert(END, line)
                    self.totLine += 1
                self.tracetape.config(state=DISABLED)
            else:
                error = tkMessageBox.showerror('Error', 'Incorrect file type!\nSelect a .data file.')

    def highlight(self):
        """TO DO"""
        self.tracetape.tag_configure('highlightline', background='red')
        self.tracetape.tag_add('highlightline', str(self.curLine), str(int(self.curLine)) + '.end') 
        if self.curLine > 1 and self.curLine <= self.totLine:
            self.tracetape.tag_remove('highlightline', str(self.curLine-1.0), str(int(self.curLine-1.0)) + '.end') 

        elif self.curLine >= self.totLine:
            self.stepButton.config(state=DISABLED)
        self.curLine += 1.0 

def main():
    """TO DO"""
    root = Tk()
    root.title("Simulation")
    root.minsize(width=600, height=620)
    root.maxsize(width=600, height=620)
    gui = MainFrame(8, root)
    root.mainloop()

if __name__ == "__main__": main()

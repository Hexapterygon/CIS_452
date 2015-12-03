#!/usr/bin/env python
"""Operating System Loader Simulation

This Python program is a text, based terminal
simulation of an operating system loader. It 
allows the user to visualize the movement of
processes, broken up into page tables, in 
and out of the available physical memory which
is broken up into frames. The simulated system
in question has 4KB of physical memory and each
page size is 512 bytes.
"""

import math
import collections
from operator import itemgetter
import os
from Tkinter import*
import ScrolledText as tkst
import tkFileDialog as tfd
import tkMessageBox

__author__ = "Nathan Anderle"
__version__ = "1.0"
__email__ = "anderlna@mail.gvsu.edu"

class Model(object):
    """Runs the logic to build the data structures"""
   
    def __init__(self, memdet):
       """Initialize some date strutures used by the simulation"""
       
       self.memdet = memdet
       self.frames = collections.OrderedDict.fromkeys(range(memdet), 'Empty')
       self.pages = []
       self.entryNum = 0


       self.trace = None 

    def frame_builder(self, procid, txtpages, datpages):
       """The frame builder takes process arrivals and puts them in physical m
       
          The frame table is implemented as an ordered dictionary (key/value
          structure that remembers the order that keys were declared) where
          each key is the frame number (0 - 8) and each key corresponds to 
          a two part array that stores [0] the procid of the owning process
          and [1] a string describing the type (text or data) and the page
          number (ex. TextPage 0, 1, etc.). The frame table is initialized
          such that each key corresponds to a None type. When frame_builder
          receives the trace tape information, it iterates over all of the 
          keys in the frame table dictionary. If the key corresponds to None,
          it is empty and the text pages of the process are stored in each 
          frame first. The data pages are then stored with the same logic.
          Finally, the frame information is passed to the page_builder such
          that each process can construct a page table with the proper frame
          information.
       """
       i = 0
       k = 0
      
       #Iterate over all the frames
       for spaces in range(0, self.memdet, 1):
                #Place all of the necessary text pages in the first empties
                if(self.frames[spaces] is 'Empty'  and i < int(txtpages)):
                    self.frames[spaces] = [procid, "Text Page " +str (i)] 
                    i += 1
                    self.page_builder(self.frames[spaces], spaces)
                #Then do all of the data pages
                elif(self.frames[spaces] is 'Empty'  and k < int(datpages)):
                    self.frames[spaces] = [procid, "Data Page " + str(k)] 
                    k += 1
                    self.page_builder(self.frames[spaces], spaces)

    def page_builder(self, frameinfo, framenum):
        """All the page tables are implemented as a list of dictionaries.
       
           Each entry in the list pages[] is a single key dictionary who's value
           is an arbitrarily (based on the needed number of pages) large array
           of strings. The key itself is the process ID and the array entries
           are descriptive strings describing the frame that a page is stored
           and the type of page. If a process does not already have a page
           table (i.e. this is the first page created for a process), this
           means that a dictionary with the particular key does not exist in
           the list. In this case, the dictionary is created and the page
           information is appended to the key. Subsequent pages for a given
           process will simply append to the dictionary with the given key
        """

        #Dictionary for process does not exist so create it
        if not any(d.get(frameinfo[0], None) for d in self.pages):
            t = {frameinfo[0] :  [str(frameinfo[1] +  " in Frame " + str(framenum))]}
            self.pages.append(t.copy())
        
        #Dictionary for process does exist, find it, and then append it
        else:
            for v in self.pages:
              z = v.keys()
              if (z[0] == frameinfo[0]):
                 self.pages[self.pages.index(v)][frameinfo[0]].append(frameinfo[1]
                         + " in Frame " + str(framenum)) 
    def delete(self, victim):
        """Set the frames containing victim pages back to None. Delete process page dict"""

        #Find the frames containing victim pages. Set them to None
        for frames in self.frames:

            if(self.frames[frames][0] != 'Empty'):

                if self.frames[frames][0] is victim:
                    self.frames[frames] = 'Empty' 
       
        #Find the dictionary that corresponds to victim. Delete it.
        for v in self.pages:
            z = v.keys()
            if(z[0] == victim):
                del self.pages[self.pages.index(v)]

    def read(self, data):
        """Read line by line a trace tape file. Each line is a list in a list"""
            
        self.trace = [line.split() for line in open (data)]
        return self.trace  

    def simulate(self):
        """simulate is the primary workhorse of the program

            simulate takes the trace tape that was read in
            as a list of lists and iterates over it. If in
            a particular entry (i.e. process event), the
            second place in the entry list is a number, it
            must be an arriving process. In this case, the
            number of frames and pages needed for the
            text/data is calculated and passed into the
            Build() class to be put into frames/pages. The
            other case is if the second place in the entry
            list is not a number. This means that the process
            event must be a halt, in which case the procid
            is sent into the Build class as a 'victim' to
            be removed from the frame table and to have its
            page table deleted.
        """

        #Process event is an arrival
        if(self.trace[self.entryNum][1].isdigit()):
            self.frame_builder(self.trace[self.entryNum][0], math.ceil((float) (self.trace[self.entryNum][1])/(512)), math.ceil((float) (self.trace[self.entryNum][2])/(512)))
            self.entryNum += 1
                
        #Process event is a halt
        else:
            self.delete(self.trace[self.entryNum][0])
            self.entryNum += 1

class MainFrame(object):
    """The primary GUI element"""

    def __init__(self, numFrames, master):
        """TO DO"""

        self.master = master
        self.numFrames = numFrames
        self.model = Model(self.numFrames)     
        self.filename = None
        self.curLine = 1.0
        self.totLine = 0
        self.piTables = []
        self.window = None 


        self.textFrame = Frame(self.master, width = 300, height = 400, bg='white')
        self.textFrame.grid(column=0, padx=20)

        self.spacerFrame = Frame(self.master, width = 50)
        self.spacerFrame.grid(row=0, column = 1)

        self.fieldFrame = Frame(self.master)
        self.fieldFrame.grid(row=0, column=2, padx=20, pady=10)
        self.labelFont = ('times', 20)

        self.pTables = []
        self.pbFrame = Frame(self.master, width=500, height=200, borderwidth = 3, relief=SUNKEN)
        self.pbFrame.grid(row=2, column=0, sticky=S, columnspan=3)
        self.pLabel = Label(self.pbFrame, text="Page Tables")
        self.rw = 0
        self.clm = 0

        for i in range(32):
            self.pTables.append(Button(self.pbFrame, height=1, width=8, text="Process "+ str(i), state=DISABLED, command=lambda i=i: self.showPage(i)))

            self.pTables[i].grid(row=self.rw, column=self.clm, sticky=W, padx=10)
            if self.clm <= 2:
                self.clm += 1
            else:
                self.rw += 1
                self.clm = 0

        self.bFrame = Frame(self.master, width=500, height=10)
        self.bFrame.grid(row=3, column=0, sticky=S, columnspan=3, pady=20)

        self.loadButton = Button(self.bFrame, text="Load", command = self.loadTrace)
        self.stepButton = Button(self.bFrame, text="Step", state=DISABLED, command= self.step)
        self.resetButton = Button(self.bFrame, text="Reset", state=DISABLED, command = self.reset) 

        self.fLabels =[]
        self.entLabels = []
        self.loadButton.grid(row=0, column=0, sticky=E)
        self.stepButton.grid(row=0, column=1, sticky=E)
        self.resetButton.grid(row=0,column=2, sticky=E)


        self.tracetape = tkst.ScrolledText(self.textFrame, width = 30, height = 20, bg='white', borderwidth = 3, relief=GROOVE, state=DISABLED)
        self.tracetape.grid()

        for i in range(numFrames):
            self.entLabels.append(Label(self.fieldFrame, width=17, text=self.model.frames[i], bg="white", fg="red", relief=GROOVE, padx=10, pady=6,  font=self.labelFont))
            self.fLabels.append(Label(self.fieldFrame, text = "Frame " + str(i), padx=5,  font=self.labelFont))
            self.fLabels[i].grid(row=i, column=0, sticky=W)
            self.entLabels[i].grid(row=i, column=1, sticky=E, columnspan=2)

    def showPage(self, num):
        self.window = Toplevel(self.master)

        entries = []

        procLabel = Label(self.window, width=31, text = "Process " + str(num), anchor=W)
        procLabel.grid(row=0, column=0, sticky=W, columnspan=3)

        spaceLabel = Label(self.window, width=10,  text =" " , relief=SUNKEN)
        spaceLabel.grid(row=1, column=0, sticky=W)
        
        pagLabel = Label(self.window, width=10,  text = "Page" , relief=SUNKEN)
        pagLabel.grid(row=1, column=1, sticky=W)

        fraLabel = Label(self.window, width=10,  text = "Frame", relief=SUNKEN)
        fraLabel.grid(row=1, column=2, sticky=W)

        rw = 2
        clm = 0

        for x in self.model.pages:
            if num == (int(x.keys()[0])):
                for z in range (len(x[str(num)])):
                    entries.append(Label(self.window, width=10, text=x[str(num)][z].split()[0], relief=SUNKEN))
                    entries.append(Label(self.window, width=10, text=x[str(num)][z].split()[2], relief=SUNKEN))
                    entries.append(Label(self.window, width=10, text=x[str(num)][z].split()[5], relief=SUNKEN))

                for v in range (len(entries)):
            
                    entries[v].grid(row=rw, column=clm)
                    if clm <= 1:
                        clm += 1
                    else:
                        rw += 1
                        clm = 0
        
        
    def loadTrace(self):
        """TO DO"""
        self.filename= tfd.askopenfilename()
        if self.filename != '':
            if self.filename.endswith('.data'):
                self.totLine = 0
                self.curLine = 1.0
                self.model.entryNum = 0
                self.stepButton.config(state=NORMAL)
                self.resetButton.config(state=NORMAL)
                self.tracetape.config(state=NORMAL)
                self.tracetape.delete(1.0, END)
                f = open(self.filename)
                for line in f:
                    self.tracetape.insert(END, line)
                    self.totLine += 1
                self.tracetape.config(state=DISABLED)
               
                self.model.read(self.filename)

            else:
                error = tkMessageBox.showerror('Error', 'Incorrect file type!\nSelect a .data file.')
        else:
            self.resetButton.config(state=DISABLED)

    def reset(self):
        if(self.filename != ''):
            self.totLine = 0
            self.curLine = 1.0
            self.model.entryNum = 0
            self.stepButton.config(state=NORMAL)
            self.tracetape.config(state=NORMAL)
            self.tracetape.delete(1.0, END)
            f = open(self.filename)
            for line in f:
                self.tracetape.insert(END, line)
                self.totLine += 1
            self.tracetape.config(state=DISABLED)
               
            self.model = Model(self.numFrames)
            self.model.read(self.filename)
            self.update()

    def step(self):
        """TO DO"""
        if self.curLine >= 1 and self.curLine <= self.totLine:
            self.highlight()
            self.model.simulate()
            self.update()

        if self.curLine >= self.totLine:
            self.stepButton.config(state=DISABLED)
        self.curLine += 1.0

    def update(self):
        """TO DO"""
        i = 0
        #Visualize the frame table using strings
        while(i < 8):
            if(self.model.frames[i] is not 'Empty' ):
                self.entLabels[i].config(text ="Process " + str(self.model.frames[i][0]) + " "  + self.model.frames[i][1])
            else:
                self.entLabels[i].config(text = "Empty")

            i += 1
            
        for x in self.model.pages:
            self.piTables.append(int(x.keys()[0])) 

        for z in range(32):
            if z in self.piTables:
                self.pTables[z].config(state=NORMAL)
            else:
                self.pTables[z].config(state=DISABLED)
        self.piTables = []

            
    def highlight(self):
        """TO DO"""
        self.tracetape.tag_configure('highlightline', background='red')
        self.tracetape.tag_add('highlightline', str(self.curLine), str(int(self.curLine)) + '.end')
        self.tracetape.tag_remove('highlightline', str(self.curLine-1.0), str(int(self.curLine-1.0)) + '.end') 

def main():
    """Main basically just sets the simulation parameters up"""
    #The number of frames
    memdet = 8

    root = Tk()
    root.title("Simulation")
    root.minsize(width=645, height=620)
    root.maxsize(width=645, height=620)
 
    gui = MainFrame(memdet, root)
    root.mainloop()

if __name__ == '__main__': main()

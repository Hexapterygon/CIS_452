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

__author__ = "Nathan Anderle"
__version__ = "1.0"
__email__ = "anderlna@mail.gvsu.edu"

class Builder(object):
    """Runs the logic to build the data structures"""
   
    def __init__(self, memdet):
       """Initialize some date strutures used by the simulation"""
       self.memdet = memdet
       self.frames = collections.OrderedDict.fromkeys(range(memdet), 'Empty')
       self.pages = []

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
                    self.frames[spaces] = [procid, "TextPage " +str (i)] 
                    i += 1
                    self.page_builder(self.frames[spaces], spaces)
                #Then do all of the data pages
                elif(self.frames[spaces] is 'Empty'  and k < int(datpages)):
                    self.frames[spaces] = [procid, "DataPage " + str(k)] 
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

        #Dictionary for process does not exise so create it
        if not any(d.get(frameinfo[0], 'Empty') for d in self.pages):
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
        print victim
        for frames in self.frames:

            if(self.frames[frames][0] != 'Empty'):

                if self.frames[frames][0] is victim:
                    self.frames[frames] = 'Empty' 
       
        #Find the dictionary that corresponds to victim. Delete it.
        for v in self.pages:
            z = v.keys()
            if(z[0] == victim):
                del self.pages[self.pages.index(v)]

class Simulate(object):
    """Run the operating system loader simulation"""
   
    def __init__(self, datafile, memdet ):
        """Initialize class variables"""
       
        self.memdet = memdet
        self.data = datafile
        self.trace = self.read() 
        self.build = Builder(self.memdet) 
    
    def read(self):
        """Read line by line a trace tape file. Each line is a list in a list"""
        try:
            self.trace = [line.split() for line in open (self.data)]
        except IOError:
            print "File does not exist"
            return 1
        else:
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
        #Allow the user to step through the program one event at a time
        raw_input("Press enter to step through Simulation")
        for entry in self.trace:

            #Process event is an arrival
            if(entry[1].isdigit()):
                self.build.frame_builder(entry[0], 
                        math.ceil((float) (entry[1])/(512)), math.ceil((float) (entry[2])/(512)))
                
                i = 0
                #Visualize the frame table using strings
                while(i < 8):
                    if(self.build.frames[i] is not 'Empty' ):
                        print "Frame " + str(i) + " Process " + str(self
                                .build.frames[i][0]) + " "  + self.build.frames[i][1]
                    else:
                        print "Frame " + str(i) + " Empty "
                    
                    i += 1
                raw_input("Press enter to step through Simulation")

            #Process event is a halt
            else:
                self.build.delete(entry[0])

                i = 0
                #Visualize the frame table using strings
                while(i < 8):
                    if(self.build.frames[i] is not 'Empty'):
                        print "Frame " + str(i) + " Process " + str(self
                                .build.frames[i][0]) + " "  + self.build.frames[i][1]
                    else:
                        print "Frame " + str(i) + " Empty "
                    
                    i += 1
                raw_input("Press enter to step through Simulation")
        
class Visualize(object):
    """Visualize is essentially a driver class that calls simulate"""

    def __init__(self, datafile, memdet):
        """This clears the screen and outputs simulation information"""
       
        self.simulate = Simulate(datafile, memdet)
        os.system('clear')
        print "System Specs: 4KB of physical memory"
        print "              512B page size"
        print "              8 frames in physical memory"
        
        self.drive()

    def drive(self):
        """Call the simulate class/method"""
        self.simulate.simulate()

def main():
    """Main basically just sets the simulation parameters up"""
    datafile = 'input2a.data'

    #The number of frames
    memdet = 8 
    driver = Visualize(datafile, memdet)

if __name__ == '__main__': main()

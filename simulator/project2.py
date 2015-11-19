#!/usr/bin/env python
"""Operating System Loader Simulation

This Python program is a graphical, interactive
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

__author__ = "Nathan Anderle"
__version__ = "1.0"
__email__ = "anderlna@mail.gvsu.edu"

class Builder(object):
    """Reads in trace tape and sets up data structures"""
   
    def __init__(self, memdet, data):
       """Initialize some date strutures used by the simulation"""
       self.trace = []
       
       if(memdet <= 50):
           self.memdet = memdet
           self.frames = collections.OrderedDict.fromkeys(range(memdet))
       else:
           raise IOError
           return 1

       self.data = data
       self.pages = []
       
    def read(self):
        """Read line by line a trace tape file. Each line is a list in a list"""
        try:
            self.trace = [line.split() for line in open (self.data)]
        except IOError:
            print "File does not exist"
            return 1
        else:
            return self.trace  

    def frame_builder(self, procid, txtpages, datpages):
       """TODO"""
       i = 0
       k = 0
       for spaces in range(0, self.memdet, 1):
                if(self.frames[spaces] is None and i < int(txtpages)):
                    self.frames[spaces] = [procid, "TextPage " +str (i)] 
                    i += 1
                    self.page_builder(self.frames[spaces], spaces)
                elif(self.frames[spaces] is None and k < int(datpages)):
                    self.frames[spaces] = [procid, "DataPage " + str(k)] 
                    k += 1
                    self.page_builder(self.frames[spaces], spaces)

    def page_builder(self, frameinfo, framenum):
        """TODO"""
        if not any(d.get(frameinfo[0], None) for d in self.pages):
            t = {frameinfo[0] :  [str(frameinfo[1] +  " in Frame " + str(framenum))]}
            self.pages.append(t.copy())
        else:
            for v in self.pages:
              z = v.keys()
              if (z[0] == frameinfo[0]):
                 self.pages[self.pages.index(v)][frameinfo[0]].append( frameinfo[1] + " in Frame " + str(framenum)) 

    def delete(self, victim):
        """TODO"""
        for frames in self.frames:
            if self.frames[frames][0] is victim:
               self.frames[frames] = 'None'
        
        for v in self.pages:
            z = v.keys()
            if(z[0] == victim):
                del self.pages[self.pages.index(v)]
class Simulate(object):
    """Run the operating system loader simulation"""
   
    def __init__(self, trace, build):
        """Initialize class variables"""
        
        self.trace = trace
        self.build = build
    
    def simulate(self):
        """TODO """
        for entry in self.trace:
            if(entry[1].isdigit()):
                self.build.frame_builder(entry[0], math.ceil((float) (entry[1])/(512)), math.ceil((float) (entry[2])/(512)))
            else:
                self.build.delete(entry[0])
        print self.build.frames
        print self.build.pages
def main():
    datafile = 'input2a.data'
    memdet = 8 

    build = Builder(memdet, datafile)
    simulate = Simulate(build.read(), build)
    
    simulate.simulate()

if __name__ == '__main__': main()

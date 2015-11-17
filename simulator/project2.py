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
__author__ = "Nathan Anderle"
__version__ = "1.0"
__email__ = "anderlna@mail.gvsu.edu"

class Setup:
    """Reads in trace tape and sets up data structures"""
   
    def __init__(self, memdet, data):
       """Initialize all the structures used by the simulation"""
       self.trace = []
       self.frames = dict.fromkeys(range(memdet))
       self.data = data

    def read(self):
        """Read line by line a trace tape file. Each line is a list in a list"""
        try:
            self.trace = [line.split() for line in open (self.data)]
         
        except IOError:
            print "File does not exist"
            return 1
        else:
            print self.trace
            return self.trace        

def main():
    datafile = 'input2a.data'
    memdet = 8 

    stuff = Setup(memdet, datafile)
    stuff.read()


if __name__ == '__main__': main()

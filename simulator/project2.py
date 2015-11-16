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

class BasicFunctionality:
    """See if I can figure out how the hell python works"""
#    def __init__(self):



    def hello(self):
        return "1Hello World"
        

def main():
    stuff = BasicFunctionality()
    stuff.hello()


if __name__ == '__main__': main()

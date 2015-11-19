#!/usr/bin/env python
"""Tests the simulator file for full functionality

    W's tied to inidividual tests implies that the 
    test is checking for something intentionally
    incorrect
"""
import unittest 
from project2 import Builder
from project2 import Simulate

__author__ = "Nathan Anderle"
__version__ = "1.0"
__email__ = "anderlna@mail.gvsu.edu"


class TestBuilder(unittest.TestCase):
    """Execute a test suite on all methods in Setup"""
  
    def test_init_args(self):
        """Are the correct # of args going to Setup?"""
        data = 'input2a.data'
        memdet = 8
        self.assertTrue(Builder(memdet, data))
        
    def test_init_wargs(self):
        """Error raised if incorrect number of args"""
        data = 'input2a.data'
        memdet = 8
        self.assertRaises(Exception, Builder, memdet)

    def test_init_memdet(self):
        """Is the physical memory determinate reasonable?"""
        data = 'input2a.data'
        memdet = 8
        self.assertTrue(Builder(memdet, data))

    def test_init_wmemdet(self):
        """Is the physical memory determinate reasonable?"""
        data = 'input2a.data'
        memdet = 1000 
        self.assertRaises(IOError, Builder, memdet, data)

    def test_read_size(self):
        """Is the file the correct size?"""
        data = 'input2a.data'
        memdet = 8
        builder = Builder(memdet, data)
        self.assertEqual(len(builder.read()), 10)
    
    def test_read_exist(self):
        """Does the data file exist?"""
        data = 'input2a.data'
        memdet = 8
        builder = Builder(memdet, data)
        self.assertTrue(builder.read())

    def test_read_handled(self):
        """Is the IOError handled correctly?"""
        data = 'garbage'
        memdet = 8
        builder = Builder(memdet, data)
        self.assertEqual(builder.read(), 1)

class TestSimulate(unittest.TestCase):
    """Test all methods in the Simulate class""" 

    def test_init_args(self):
        """Test the number of args to Simulate"""
        trace = [1,2,3,4,5]  
        data = 'input2a.data'
        memdet = 8
        builder = Builder(memdet, data)
        self.assertTrue(Simulate(trace, builder))


if __name__ == '__main__': 
    unittest.main()


#!/usr/bin/env python
"""Tests the simulator file for full functionality
"""
import unittest 
from project2 import Setup

__author__ = "Nathan Anderle"
__version__ = "1.0"
__email__ = "anderlna@mail.gvsu.edu"


class TestSetup(unittest.TestCase):
    """Execute a test suite on all methods in Setup"""
  
    def test_init_args(self):
        """Are the correct # of args going to Setup?"""
        data = 'input2a.data'
        memdet = 8
        self.assertTrue(Setup(memdet, data))
        
    def test_init_wargs(self):
        """Error raised if incorrect number of args"""
        data = 'input2a.data'
        memdet = 8
        self.assertRaises(Exception, Setup, memdet)

    def test_read_size(self):
        """Is the file the correct size?"""
        data = 'input2a.data'
        memdet = 8
        setup = Setup(memdet, data)
        self.assertEqual(len(setup.read()), 10)
    
    def test_read_exist(self):
        """Does the data file exist?"""
        data = 'input2a.data'
        memdet = 8
        setup = Setup(memdet, data)
        self.assertTrue(setup.read())

    def test_read_handled(self):
        """Is the IOError handled correctly?"""
        data = 'garbage'
        memdet = 8
        setup = Setup(memdet, data)
        self.assertEqual(setup.read(), 1)


if __name__ == '__main__': 
    unittest.main()


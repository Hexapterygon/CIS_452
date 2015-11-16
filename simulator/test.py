#!/usr/bin/env python
"""Tests the simulator file for full functionality
"""
import unittest 
from project2 import BasicFunctionality

__author__ = "Nathan Anderle"
__version__ = "1.0"
__email__ = "anderlna@mail.gvsu.edu"

basic = BasicFunctionality()

class BasicTestCase(unittest.TestCase):
    """See if I can figure out how to python testi"""

    def test_is_hello(self):
        """does hello return "Hello World"?"""
        self.assertEqual(basic.hello(), "Hello World")


if __name__ == '__main__': 
    unittest.main()


#!/usr/bin/env python

from selenese import convert_selenese, unittest
import sys

DEBUG = False
try:
    if sys.argv[1] == "debug": 
        DEBUG = True
        sys.argv.pop(1)
except IndexError:
    pass

# Test basic multi-file tests
BasicTests = convert_selenese("tests", "http://github.com/", DEBUG)
# Also test more than one class
SecondTest = convert_selenese("tests/secondtest", "http://github.com/", DEBUG)

unittest.main()

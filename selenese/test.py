#!/usr/bin/env python

from selenese import convert_selenese, unittest
import sys

try:
    s = sys.argv[1]
    sys.argv.pop(1)
except IndexError:
    s = "localhost"

try:
    DEBUG = (sys.argv[2] == "debug")
    sys.argv.pop(2)
except IndexError:
    DEBUG = False

# Test basic multi-file tests
BasicTests = convert_selenese("tests", "github.com", s, DEBUG)
# Also test more than one class
SecondTest = convert_selenese("tests/secondtest", "github.com", s, DEBUG)
# Test supported actions
ActionsTest = convert_selenese("tests/actions", "github.com", s, DEBUG)

unittest.main()

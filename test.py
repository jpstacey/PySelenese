#!/usr/bin/env python

from selenese import convert_selenese, unittest

# Test basic multi-file tests
BasicTests = convert_selenese("tests", "http://github.com/")
# Also test more than one class
SecondTest = convert_selenese("tests/secondtest", "http://github.com/")
# Test unknown keywords
import tests.test_unknown

unittest.main()

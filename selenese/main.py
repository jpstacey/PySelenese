#!/usr/bin/env python

import sys
from selenese import convert_selenese, unittest

def main():
    try:
        convert_dir = sys.argv[1]
        sys.argv.pop(1)
    except IndexError:
        convert_dir = "."
    try:
        u = sys.argv[1]
        sys.argv.pop(1)
    except IndexError:
        u = "localhost"
    MyTest = convert_selenese(convert_dir, u)
    # Run test suite, picking up on ConvertedTest().test_N for all tests N
    unittest.main()

if __name__ == "__main__":
    main()

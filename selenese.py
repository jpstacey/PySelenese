#!/usr/bin/env python

from lxml import etree
import unittest

DEBUG = False

def get_html_title(tree, default = "Untitled"):
    """Return a decent title from the current HTML page tree"""
    try:
        return tree.find("/head/title").text
    except AttributeError:
        return default

def run_html_test(title, table, obj):
    # The engine for running Selenium HTML in Python
    # TODO More code here!
    pass

class ConvertedTest(unittest.TestCase):
    """Container class for storing Selenium HTML converted tests"""
    pass

p = etree.HTMLParser()
x = etree.parse('../index.html', p)
if DEBUG: print "Examining test suite: %s" % get_html_title(x)

i = 0
for test in x.findall("//table[@id='suiteTable']//tr//a"):
    # Get HTML file for test
    x_test = etree.parse("../"+test.get("href"), p)
    test_title = get_html_title(x_test)
    if DEBUG: print "    Converting test: %s" % test_title

    # Find test table
    test_table = x_test.find("/body//table")
    if test_table != None:
        # Create a lambda function, give it a __doc__ so reporting is verbose
        fn = lambda obj: run_html_test(test_title, test_table, obj)
        fn.__setattr__("__doc__", test_title)
        # Now add it to the ConvertedTest class as an object method test_N
        type(ConvertedTest).__setattr__(ConvertedTest, "test_%d" % i, fn)
        i+=1

# Run test suite, picking up on ConvertedTest().test_N for all tests N
unittest.main()

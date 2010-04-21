#!/usr/bin/env python

from lxml import etree
import unittest

p = etree.HTMLParser()
x = etree.parse('index.html', p)

def get_html_title(tree):
    try:
        return tree.find("/head/title").text
    except AttributeError:
        return "Untitled"

class ConvertedTest(unittest.TestCase):
    def __init__(self, *kw, **args):
        unittest.TestCase.__init__(self, *kw, **args)

print "Examining test suite: %s" % get_html_title(x)

def run_html_test(title, table, obj):
    # The engine for running Selenium tests
    pass

i = 0
for test in x.findall("//table[@id='suiteTable']//tr//a"):
    # Get HTML file for test
    x_test = etree.parse(test.get("href"), p)
    test_title = get_html_title(x_test)
    print "    Converting test: %s" % test_title

    # Find test table
    test_table = x_test.find("/body//table")
    if test_table:
        fn = lambda obj: run_html_test(test_title, test_table, obj)
        fn.__setattr__("__doc__", test_title)
        type(ConvertedTest).__setattr__(ConvertedTest, "test_%d" % i, fn)
        i+=1

unittest.main()

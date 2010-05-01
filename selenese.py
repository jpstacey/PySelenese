#!/usr/bin/env python

import os
import unittest

from copy import deepcopy
from lxml import etree
from selenium import selenium

from mapper import SeleniumMapper

import inspect

DEBUG = True

class PySeleneseError(Exception):
    pass

def get_html_title(tree, default = "Untitled"):
    """Return a decent title from the current HTML page tree"""
    try:
        return tree.find("/head/title").text
    except AttributeError:
        return default

def run_html_test(obj):
    """As a lambda function this is an engine for running lxml Selenese

    table is an lxml document fragment; obj is the TestCase object"""

    # The only way we can "pass" the relevant HTML into a lambda function is
    # to attach all of them to the test case, then work out the index from
    # the function name
    try:
        index = int(obj._testMethodName.replace("test_", ""))
        table = obj.test_tables[index]
    except ValueError:
        raise PySeleneseError("Can't work out which file this test function came from.")
    except AttributeError:
        raise PySeleneseError("Can't work out what my test function is called: has unittest.py changed?")
    except KeyError:
        raise PySeleneseError("I think I'm test #%d but my test class doesn't have the HTML for that." % index)

    for instruction in table.findall(".//tr"):
        args = instruction.findall("td")
        # Only call text if we've got at least the core 3 Selense <td>s
        if len(args) > 2:
            args = [a.text for a in args]
            # Add a possible documenting string
            (len(args) > 3) or args.append('')

            cmd = args.pop(0)
            try:
                obj.mapper.__getattribute__(cmd)
            except AttributeError:
                raise PySeleneseError("Selenese command '%s' not implemented yet, or maybe a syntax error." % cmd)
            obj.mapper.__getattribute__(cmd)(args)

def new_sel(domain):
    """Create Selenium instance with defaults"""
    sel = selenium("localhost", 4444, "*firefox", "http://%s/" % domain)
    sel.start()
    return sel

class GenericTest(unittest.TestCase):
    root_url = "github.com"

    test_tables = {}

    """Container class for storing converted Selenese tests"""
    def setUp(self):
        self.selenium = new_sel(self.root_url)
        self.selenium.test = self
        self.mapper = SeleniumMapper(self)

    def tearDown(self):
        self.selenium.stop()

def convert_selenese(my_dir='.', _root_url = None):
    """Returns a unittest.TestCase subclass for testing"""

    # Find and parse index.html test suite
    old_dir = os.getcwd()
    os.chdir(my_dir)
    p = etree.HTMLParser()
    x = etree.parse('index.html', p)
    if DEBUG: print "Examining test suite: %s" % get_html_title(x)

    # Set up a test class to return from the function
    class ConvertedTest(GenericTest): pass
    if _root_url: ConvertedTest.root_url = _root_url

    i = 0
    test_tables = {}
    for test in x.findall("//table[@id='suiteTable']//tr//a"):
        # Get HTML file for test
        x_test = etree.parse(test.get("href"), p)
        test_title = get_html_title(x_test)

        # Find test table
        test_table = x_test.find("/body//table")
        if test_table != None:
            if DEBUG: print "    Converting test: %s" % test_title

            test_tables[i] = test_table
            # Create a lambda function, give it a __doc__ so reporting is verbose
            fn = lambda obj: run_html_test(obj)
            fn.__setattr__("__doc__", test_title)
            fn.__setattr__("_selenium_index", i)
            # Now add it to the ConvertedTest class as an object method test_N
            type(ConvertedTest).__setattr__(ConvertedTest, "test_%d" % i, fn)
            i+=1

    ConvertedTest.test_tables = test_tables

    # Reset the directory and return our completed TestCase
    os.chdir(old_dir)
    return ConvertedTest


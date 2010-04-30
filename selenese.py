#!/usr/bin/env python

import os
import unittest

from copy import deepcopy
from lxml import etree
from selenium import selenium

from mapper import SeleniumMapper

DEBUG = True

def get_html_title(tree, default = "Untitled"):
    """Return a decent title from the current HTML page tree"""
    try:
        return tree.find("/head/title").text
    except AttributeError:
        return default

def run_html_test(table, obj):
    """As a lambda function this is an engine for running lxml Selenese

    table is an lxml document fragment; obj is the TestCase object"""
    for instruction in table.findall(".//tr"):
        args = instruction.findall("td")
        # Only call text if we've got at least the core 3 Selense <td>s
        if len(args) > 2:
            args = [a.text for a in args]
            # Add a possible documenting string
            (len(args) > 3) or args.append('')

            cmd = args.pop(0)
            obj.mapper.__getattribute__(cmd)(args)

def new_sel(domain):
    """Create Selenium instance with defaults"""
    sel = selenium("localhost", 4444, "*firefox", "http://%s/" % domain)
    sel.start()
    return sel

class GenericTest(unittest.TestCase):
    root_url = "github.com"

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
    for test in x.findall("//table[@id='suiteTable']//tr//a"):
        # Get HTML file for test
        x_test = etree.parse(test.get("href"), p)
        test_title = get_html_title(x_test)

        # Find test table
        test_table = x_test.find("/body//table")
        if test_table != None:
            if DEBUG: print "    Converting test: %s" % test_title

            # Create a lambda function, give it a __doc__ so reporting is verbose
            fn = lambda obj: run_html_test(test_table, obj)
            fn.__setattr__("__doc__", test_title)
            # Now add it to the ConvertedTest class as an object method test_N
            type(ConvertedTest).__setattr__(ConvertedTest, "test_%d" % i, fn)
            i+=1

    # Reset the directory and return our completed TestCase
    os.chdir(old_dir)
    return ConvertedTest


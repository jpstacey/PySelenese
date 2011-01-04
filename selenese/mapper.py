#!/usr/bin/env python

import re

class MapperException(Exception):
    """Excecptions in mapper layer"""
    pass

def _camelcase_to_underscore(text):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class SeleniumMapper(object):
    """Maps Selenium commands to Selenese <td> contents"""

    # Master debug setting in selenese.py - suggest you change it there
    DEBUG = False

    def __init__(self, test):
        self.test = test
        self.sel = test.selenium

    # Trans-parent introspection - if the method exists on the child self.sel
    # object, but NOT on this object, then these two methods introspect through to 
    # the child's method, work out its arg count, and "just" call it.
    def __getattribute__(self, name):
        try:
            # Does the method exist on SeleniumMapper i.e. self?
            return object.__getattribute__(self, name)
        except AttributeError, e:
            # If not, try to get from the child self.sel object
            sel_method = self.sel.__getattribute__(name)
            # Wrap in a lambda so we can call it safely with args
            # based on the number of <td>s rather than the method
            # signature - see below
            return lambda args: self.__call_sel__(sel_method, args)

    def __call_sel__(self, sel_method, args):
        # Use introspection on the underlying Selenium method
        # The first argument is the self object so ignore
        num_args = sel_method.im_func.func_code.co_argcount - 1
        # Now whittle our args down so it matches the method signature
        args = args[:num_args]
        # ... And call!
        sel_method(*args)

    def addScript(self, args):
        self.sel.add_script(args[0], args[1])

    def allowNativeXpath(self, args):
        self.sel.allow_native_xpath(args[0])

    def answerOnNextPrompt(self, args):
        self.sel.answer_on_next_prompt(args[0])

    """Set: assert"""
    def assertAlert(self, args):
        self.test.assertEquals(self.sel.get_alert(), args[0], args[2])

    def assertElementPresent(self, args):
        self.test.assert_(self.sel.is_element_present(args[0]), args[2])

    def assertHtmlSource(self, args):
        self.test.assertEquals(self.sel.get_html_source(), args[0], args[2])

    def assertTextNotPresent(self, args):
        self.test.assert_(not self.sel.is_text_present(args[0]), args[2])

    def assertTextPresent(self, args):
        self.test.assert_(self.sel.is_text_present(args[0]), args[2])

    def assertXpathCount(self, args):
        self.test.assertEquals(self.sel.get_xpath_count(args[0]), args[1], args[2])

    def click(self, args):
        self.sel.click(args[0])

    def clickAndWait(self, args):
        self.sel.click(args[0])
        self.sel.wait_for_page_to_load(30000)

    def _debug(self, args):
        """Debugging"""
        if self.DEBUG: print args[2]

    def deleteAllVisibleCookies(self, args):
        self.sel.delete_all_visible_cookies()

    def _fail(self, args):
        """Selenese does not have a native fail, but it can come in handy for debugging"""
        self.test.fail(args[2])

    def open(self, args):
        # Warning: Selenese tests don't mind 404s; Selenium RC does
        self.sel.open(args[0])

    def runScript(self, args):
        self.sel.run_script(args[0])

    def select(self, args):
        self.sel.select(args[0], args[1])

    def type(self, args):
        self.sel.type(args[0], args[1])

    """Set: verify"""
    def verifyElementPresent(self, args):
        self.test.assert_(self.sel.is_element_present(args[0]), args[2])

    def verifyTextPresent(self, args):
        self.test.assert_(self.sel.is_text_present(args[0]), args[2])

    def waitForPageToLoad(self, args):
        self.sel.wait_for_page_to_load(30000)

if __name__ == '__main__':
    print "\n".join([a for a in dir(SeleniumMapper) if a[0:2] != "__"])

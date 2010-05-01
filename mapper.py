#!/usr/bin/env python

class SeleniumMapper(object):
    """Maps Selenium commands to Selenese <td> contents"""
    def __init__(self, test):
        self.test = test
        self.sel = test.selenium

    def open(self, args):
        # Warning: Selenese tests don't mind 404s; Selenium RC does
        self.sel.open(args[0])

    def assertXpathCount(self, args):
        self.test.assertEquals(self.sel.get_xpath_count(args[0]), args[1], args[2])

    def assertHtmlSource(self, args):
        self.test.assertEquals(self.sel.get_html_source(), args[0], args[2])

    def assertTextNotPresent(self, args):
        self.test.assert_(not self.sel.is_text_present(args[0]), args[2])

    def assertTextPresent(self, args):
        self.test.assert_(self.sel.is_text_present(args[0]), args[2])

    def click(self, args):
        self.sel.click(args[0])

    def clickAndWait(self, args):
        self.sel.click(args[0])
        self.sel.wait_for_page_to_load(30000)

    def _debug(self, args):
        """Debugging"""
        print args[2]

    def _fail(self, args):
        """Selenese does not have a native fail, but it can come in handy for debugging"""
        self.test.fail(args[2])

    def deleteAllVisibleCookies(self, args):
        self.sel.delete_all_visible_cookies()

    def type(self, args):
        self.sel.type(args[0], args[1])

if __name__ == '__main__':
    print "\n".join([a for a in dir(SeleniumMapper) if a[0:2] != "__"])

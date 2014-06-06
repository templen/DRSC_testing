#! /usr/bin/python

from selenium import webdriver
import unittest
import sys

devel_mode = False # True if we are testing development site

def DRSC_URL(more = ''):
    if more and more[0] != '/':
        more = '/' + more
    if devel_mode:
        return "http://dev.www.flyrnai.org" + more
    else:
        return "http://www.flyrnai.org" + more




class DIOPTTest(unittest.TestCase):

    def setUp(self): #2
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self): #3
        self.browser.quit()

    def test_does_the_title_match_the_page_title(self):
        # standard question - is the page title correct for this page
        # (or did we forget to update it when we copied the code for
        # this page from somewhere else?)
        self.browser.get(DRSC_URL("DIOPT"))
        self.assertIn("DRSC Integrative Ortholog Prediction Tool",
                      self.browser.title)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[-1].lower() == "-d":
            devel_mode = True
        elif sys.argv[-1].lower() == "-p":
            devel_mode = False
    unittest.main()

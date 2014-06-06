#! /usr/bin/python

from selenium import webdriver
import unittest

class DIOPTTest(unittest.TestCase):

    def setUp(self): #2
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self): #3
        self.browser.quit()


"""
All tests will have setUp and tearDown. TestFixtures ensures that each test case
have both setUp and tearDown.

"""

import unittest
from selenium import webdriver
from selenium_driver import SeleniumDriver
from string_constants import *
from test_operation import *
import time


class TestFixtures(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        ipAddress = get_ip_addresses()
        self.baseUrl = ipAddress[0]
        try:
            self.driver.get(self.baseUrl)
        except:
            print "Invalid IP Address"

    def tearDown(self):
        print "\nTest Complete"
        time.sleep(5)
        self.driver.quit()
        print "\n--------------------------------------------\n"

    def is_hidden_string(self, element):
        driver = SeleniumDriver(self.driver)

        driver.getElement(element, XPATH)
        element_class = driver.getElementAttribute(element, XPATH, ClASS)

        if 'hidden' in element_class:
            return True
        else:
            return False

    def has_error(self, inputBox):
        driver = SeleniumDriver(self.driver)

        driver.getElement(inputBox, XPATH)
        inputBoxClass = driver.getElementAttribute(inputBox, XPATH, ClASS)

        if 'has-error' in inputBoxClass:
            return True
        else:
            return False

    
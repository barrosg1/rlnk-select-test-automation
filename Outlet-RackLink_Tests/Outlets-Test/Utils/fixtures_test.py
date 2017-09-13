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

    def is_hidden_string(self, element):
        """

        :param element: the current element (XPATH)
        :return: returns true if 'hidden' is in the element's class
        """
        driver = SeleniumDriver(self.driver)

        driver.get_element(element, XPATH)
        element_class = driver.get_element_attribute(element, XPATH, ClASS)

        if 'hidden' in element_class:
            return True
        else:
            return False

    def is_on(self, element):
        """

        :param element: the current element (XPATH)
        :return: returns true if 'state-on' or 'state1' is in the element's class
        """
        driver = SeleniumDriver(self.driver)

        driver.get_element(element, XPATH)
        element_class = driver.get_element_attribute(element, XPATH, ClASS)

        if 'state-on' in element_class or 'state1' in element_class:
            return True
        else:
            return False


    def has_error(self, inputBox):
        """

        :param inputBox: the section where users send input strings
        :return: returns true if 'has-error' is in the inputBox class
        """
        driver = SeleniumDriver(self.driver)

        driver.get_element(inputBox, XPATH)
        inputBoxClass = driver.get_element_attribute(inputBox, XPATH, ClASS)

        if 'has-error' in inputBoxClass:
            return True
        else:
            return False

    
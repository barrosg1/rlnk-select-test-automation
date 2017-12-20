"""
All tests will have setUp and tearDown. TestFixtures ensures that each test case
have both setUp, tearDown, and mostly used functions to perform during the tests.


Note: IE version 9 and onwards does not accept username and password in the url for example:

    http://username:password@192.168.0.34 will NOT work

To run the test on different browsers (IE, Chrome, Firefox, Edge) in parallel, Selenium Standalone Server must be
used. See http://www.seleniumhq.org/download/ for more information.

"""

import unittest
from selenium import webdriver
from selenium_driver import SeleniumDriver
from string_constants import *
from test_operation import *
import time

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# create capabilities
capabilities = DesiredCapabilities.INTERNETEXPLORER

# delete platform and version keys
capabilities.pop("platform", None)
capabilities.pop("version", None)

class TestFixtures(unittest.TestCase):

    def setUp(self):
        try:
            # Different browsers to test
            self.driver = webdriver.Chrome()
            #self.driver = webdriver.Firefox()
            #self.driver = webdriver.Ie()

            self.driver.maximize_window()

            self.baseUrl = get_uut_addresses()[0]
            self.driver.get(self.baseUrl)

            self.driver.implicitly_wait(10)
        except:
            print "Could not open url (" + self.baseUrl + ")."

    def tearDown(self):
        time.sleep(4)
        self.driver.quit()

    # ----------------------------- most used functions -----------------------------

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

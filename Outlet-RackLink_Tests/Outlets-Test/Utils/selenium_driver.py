"""
Custom Selenium driver class

All member methods of the SeleniumDriver class takes care of repetitive tasks
from Selenium

Example 1: instead of using self.driver.find_element_by_id("element_id")
         Use driver.get_element('element_id', 'id')

Example 2: instead of using self.driver.find_element_by_xpath('//div[8]/button').click()
           Use driver.elementClick('//div[8]/button', 'xpath')

"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *


class SeleniumDriver:
    def __init__(self, driver):
        self.driver = driver

    def get_by_type(self, locator_type):
        """
        Function that retrieves a locator by type

        :param locator_type: id, xpath, class, css, link text
        :return: Should return a locator by type

        """

        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "classname":
            return By.CLASS_NAME
        elif locator_type == "linktext":
            return By.LINK_TEXT
        else:
            print("\nLocator type " + locator_type + " not correct/supported")
        return False

    def get_element(self, locator, locator_type):
        try:
            locator_type = locator_type.lower()
            byType = self.get_by_type(locator_type)
            element = self.driver.find_element(byType, locator)
        except NoSuchElementException:
            return False
        return element

    def element_click(self, locator, locator_type):
        """
        Function to click on an element

        :param locator: a string
        :param locator_type: id, xpath, class, css, link text

        """
        try:
            element = self.get_element(locator, locator_type)
            element.click()
        except NoSuchElementException:
            print("\nCannot click on the element with locator: " + locator + " locator_type: " + locator_type)

    def is_element_present(self, locator, byType):
        """
        Function that checks if an element is present

        :param locator: a string
        :param byType: id, xpath, class, css, link text

        """
        try:
            element = self.driver.find_element(byType, locator)
            if element is not None:
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def is_element_selected(self, locator, byType):
        """
        Function to check if an element is selected

        :param locator: a string
        :param byType: id, xpath, class, css, link text

        """

        try:
            element = self.driver.find_element(byType, locator)
            if element.is_selected():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def wait_until_clickable(self, locator, locator_type="id"):
        """
        Function waits for an element to be clickable

        :param locator: a string
        :param locator_type: id, xpath, class, css, link text
        :param timeout: time (in seconds) to wait for an element to be clickable
        :param pollFrequency: how frequent (in seconds) it will try to poll the element
        :return: returns the desired element

        """

        element = None
        try:
            byType = self.get_by_type(locator_type)
            wait = WebDriverWait(self.driver, 10, poll_frequency=0.5,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
        except ElementNotVisibleException:
            print("\nElement " + str(locator) + " did not appear on the web page")
        return element

    def wait_for_visibility(self, locator, locator_type="id"):
        """
        Function waits for element to be both present in the DOM and visible on the UI

        :param locator: a string
        :param locator_type: id, xpath, class, css, link text
        :param timeout: time (in seconds) to wait for an element to be clickable
        :param pollFrequency: how frequent (in seconds) it will try to poll the element
        :return: returns the desired element

        """

        element = None
        try:
            byType = self.get_by_type(locator_type)
            wait = WebDriverWait(self.driver, 10, poll_frequency=0.5)
            element = wait.until(EC.visibility_of_element_located((byType, locator)))
        except ElementNotVisibleException:
            print("\nElement " + str(locator) + " did not appear on the web page")
        return element

    def wait_for_presence_of_element(self, locator, locator_type="id"):
        """
        Function waits for element to be both present in the DOM and visible on the UI

        :param locator: a string
        :param locator_type: id, xpath, class, css, link text
        :return: returns the desired element

        """

        element = None
        try:
            byType = self.get_by_type(locator_type)
            wait = WebDriverWait(self.driver, 10, poll_frequency=0.5)
            element = wait.until(EC.presence_of_element_located((byType, locator)))
        except ElementNotVisibleException:
            print("\nElement " + str(locator) + " did not appear on the web page")
        return element

    def wait_for_invisibility(self, locator, locatorType="id"):
        """
        Function waits for element to be invisible in the DOM and invisible on the UI

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text
        :return: returns the desired element

        """

        element = None
        try:
            byType = self.get_by_type(locatorType)
            wait = WebDriverWait(self.driver, 10, poll_frequency=0.5)
            element = wait.until(EC.invisibility_of_element_located((byType, locator)))
        except ElementNotVisibleException:
            print("\nElement " + str(locator) + " did not appear on the web page")
        return element

    def wait_text_to_be_present_in_elem(self, locator, locatorType, text, timeout):
        """
        Function waits for element to be invisible in the DOM and invisible on the UI

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text
        :param text: a text
        :param timeout: time (in seconds) to wait for an element to be clickable
        :return: returns the desired element

        """

        element = None
        try:
            byType = self.get_by_type(locatorType)
            wait = WebDriverWait(self.driver, timeout, poll_frequency=0.5)
            element = wait.until(EC.text_to_be_present_in_element((byType, locator), text))
        except ElementNotVisibleException:
            print("\nElement " + str(locator) + " did not appear on the web page")
        return element

    def wait_and_click(self, locator, locatorType):

        """
        Function waits for an element to be present and then click on the element

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text

        """

        try:
            element = self.get_element(locator, locatorType)
            self.wait_until_clickable(locator, locatorType)
            element.click()
        except NoSuchElementException:
            print("\nCannot click on the element with locator: " +
                  locator + " locatorType: " + locatorType)

    def send_input(self, locator, locatorType, input_string):
        """
        Function to send keys to an input element

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text
        :param input_string: any input string
        :return: an input value

        """

        try:
            self.wait_for_visibility(locator, locatorType)
            sendInputIn = self.get_element(locator, locatorType)
            sendInputIn.clear()
            sendInputIn.send_keys(input_string)
        except NoSuchElementException:
            return False

    def get_element_attribute(self, locator, locatorType, attribute):
        """
        Function to get a specific element attribute

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text
        :param attribute: specific attribute from an element
        :return: an attribute
        """
        elementAttr = None
        try:
            elementAttr = self.get_element(locator, locatorType).get_attribute(attribute)
        except NoSuchElementException:
            return False
        return elementAttr

    def force_click(self, locator, locatorType):
        """
        If an element can't be click with the standar click() function
        then try to force click the element. (mostly used with list <li> in this project)

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text

        """
        try:
            elem = self.get_element(locator, locatorType)
            actions = ActionChains(self.driver)
            actions.move_to_element(elem)
            actions.click(elem)
            actions.perform()
        except NoSuchElementException:
            print("\nCannot click on the element with locator: " +
                  locator + " locatorType: " + locatorType)

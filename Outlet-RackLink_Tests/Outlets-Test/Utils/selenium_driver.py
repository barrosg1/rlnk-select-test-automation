"""
Custom Selenium driver class

All member methods of the SeleniumDriver class takes care of repetitive tasks
from Selenium

Example 1: instead of using self.driver.find_element_by_id("element_id")
         Use driver.getElement("element_id", "id")

Example 2: instead of using self.driver.find_element_by_xpath("//div[8]/button").click()
           Use driver.elementClick("//div[8]/button", "xpath")

"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *


class SeleniumDriver:
    def __init__(self, driver):
        self.driver = driver

    def locatorFound(self, locator):
        # print("\nElement " + '"' + str(locator) + '"' + " was found")
        pass

    def locatorNotFound(self, locator):
        print("\nElement " + '"' + str(locator) + '"' + " was not found")

    def getByType(self, locatorType):
        """
        Function that retrieves a locator by type

        :param locatorType: id, xpath, class, css, link text
        :return: Should return a locator by type

        """

        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "classname":
            return By.CLASS_NAME
        elif locatorType == "linktext":
            return By.LINK_TEXT
        else:
            print("\nLocator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType):
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
        except NoSuchElementException:
            self.locatorNotFound(locator)
            return False
        return element

    def elementClick(self, locator, locatorType):
        """
        Function to click on an element

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text

        """
        try:
            element = self.getElement(locator, locatorType)
            element.click()
        except NoSuchElementException:
            print("\nCannot click on the element with locator: " + locator + " locatorType: " + locatorType)

    def isElementPresent(self, locator, byType):
        """
        Function that checks if an element is present

        :param locator: a string
        :param byType: id, xpath, class, css, link text

        """
        try:
            element = self.driver.find_element(byType, locator)
            if element is not None:
                self.locatorFound(locator)
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def isElementSelected(self, locator, byType):
        """
        Function to check if an element is selected

        :param locator: a string
        :param byType: id, xpath, class, css, link text

        """

        try:
            element = self.driver.find_element(byType, locator)
            if element.is_selected():
                self.locatorFound(locator)
                return True
            else:
                self.locatorNotFound(locator)
                return False
        except NoSuchElementException:
            self.locatorNotFound(locator)
            return False

    def waitUntilClickable(self, locator, locatorType="id",
                           timeout=10, pollFrequency=0.5):
        """
        Function waits for an element to be clickable

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text
        :param timeout: time (in seconds) to wait for an element to be clickable
        :param pollFrequency: how frequent (in seconds) it will try to poll the element
        :return: returns the desired element

        """

        element = None
        try:
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, 10, poll_frequency=0.5,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
        except ElementNotVisibleException:
            print("\nElement " + str(locator) + " did not appear on the web page")
        return element

    def waitForVisibility(self, locator, locatorType="id",
                           timeout=10, pollFrequency=0.5):
        """
        Function waits for element to be both present in the DOM and visible on the UI

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text
        :param timeout: time (in seconds) to wait for an element to be clickable
        :param pollFrequency: how frequent (in seconds) it will try to poll the element
        :return: returns the desired element

        """

        element = None
        try:
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, 10, poll_frequency=0.5,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((byType, locator)))
        except ElementNotVisibleException:
            print("\nElement " + str(locator) + " did not appear on the web page")
        return element

    def waitAndClick(self, locator, locatorType,
                     timeout=10, pollFrequency=0.5):

        """
        Function waits for an element to be present and then click on the element

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text
        :param timeout: time (in seconds) to wait for an element to be clickable
        :param pollFrequency: how frequent (in seconds) it will try to poll the element

        """

        try:
            element = self.getElement(locator, locatorType)
            self.waitUntilClickable(locator, locatorType)
            element.click()
        except NoSuchElementException:
            print("\nCannot click on the element with locator: " +
                  locator + " locatorType: " + locatorType)

    def sendInput(self, locator, locatorType, inputString):
        """
        Function to send keys to an input element

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text
        :param inputString: any input string
        :return: an input value

        """

        sendInputIn = None
        try:
            self.waitUntilClickable(locator, locatorType)
            sendInputIn = self.getElement(locator, locatorType)
            sendInputIn.clear()
            sendInputIn.send_keys(inputString)
        except NoSuchElementException:
            self.locatorNotFound(locator)
        return sendInputIn

    def getElementAttribute(self, locator, locatorType, attribute):
        """
        Function to get a specific element attribute

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text
        :param attribute: specific attribute from an element
        :return: an attribute
        """
        elementAttr = None
        try:
            elementAttr = self.getElement(locator, locatorType).get_attribute(attribute)
        except NoSuchElementException:
            self.locatorNotFound(locator)
        return elementAttr

    def forceClick(self, locator, locatorType):
        """
        If an element can't be click with the standar click() function
        then try to force click the element. (mostly used with list <li> in this project)

        :param locator: a string
        :param locatorType: id, xpath, class, css, link text

        """
        try:
            elem = self.getElement(locator, locatorType)
            actions = ActionChains(self.driver)
            actions.move_to_element(elem)
            actions.click(elem)
            actions.perform()
        except NoSuchElementException:
            print("\nCannot click on the element with locator: " +
                  locator + " locatorType: " + locatorType)

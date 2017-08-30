import sys
import time

from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletNameChange(TestFixtures):
    def test_outlet_name(self):
        self.outlet_name_not_changed()
        self.outlet_name_blank()
        self.outlet_name_length()

    def outlet_name_not_changed(self):
        """
        Click on the outlet
        verify that the name has not changed after clicking the cancel btn.

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletNameElement = '//div[8]/div[2]/input'

        randomInput = "Outlet Name"

        index = 2
        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            outletBoxStr = ".//*[@id='outletControl']/div[{0}]".format(index)
            time.sleep(5)
            outletBox.click()
            driver.waitForElement(outletNameElement, XPATH)
            driver.sendInput(outletNameElement, XPATH, randomInput)

            driver.waitAndClick(cancel_btn_xpath(), XPATH)

            time.sleep(3)
            driver.waitAndClick(outletBoxStr, XPATH)

            driver.waitForElement(outletNameElement, XPATH)
            driver.getElement(outletNameElement, XPATH)

            inputVal = driver.getElementAttribute(outletNameElement, XPATH, VALUE)

            assert inputVal != randomInput
            print "Name didn't change after clicking the cancel button |  PASSED"

            driver.waitAndClick(cancel_btn_xpath(), XPATH)
            index += 1
            outletCount += 1

        time.sleep(8)

    def outlet_name_blank(self):
        """
        Verify that the name input box has a red border
        after changing the name to blank/empty

        """

        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletNameElement = '//div[8]/div[2]/input'
        notify = ".//*[@id='notify']"
        expectedOpGood = False

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()
            driver.waitForElement(outletNameElement, XPATH)
            driver.getElement(outletNameElement, XPATH).clear()

            driver.waitAndClick(outlet_save_btn(), XPATH)

            notifyVisible = driver.isElementPresent(notify, XPATH)
            assert notifyVisible == True
            print "Notification message appeared |  PASSED"

            driver.getElement(outletNameElement, XPATH)

            outletNameElementClass = driver.getElementAttribute(outletNameElement, XPATH, ClASS)
            if 'has-error' in outletNameElementClass:
                expectedOpGood = True
                driver.waitAndClick("btnOk", ID)

            driver.waitAndClick(cancel_btn_xpath(), XPATH)

            assert expectedOpGood == True
            print "Input box has a red border |  PASSED"

            outletCount += 1
        time.sleep(8)

    def outlet_name_length(self):
        """
        function to test outlets' name
        outlet name can only accept up to 50 characters (letters, digits, and special characters)

        """

        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletNameElement = '//div[8]/div[2]/input'

        # Random characters with a length of 50 to test outlet's name
        randomChars = 'g#QUfjeTakWbxHCS*6RQ579Wq6sBV3AT?#T!DrZ6#yJpbZzC$@'

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()
            driver.waitForElement(outletNameElement, XPATH)
            driver.sendInput(outletNameElement, XPATH, randomChars)

            driver.waitAndClick(outlet_save_btn(), XPATH)
            inputValue = driver.getElementAttribute(outletNameElement, XPATH, VALUE)

            #  assert input
            assert 50 >= len(inputValue) >= 1
            print "Input value is under 50 characters |  PASSED"
            print "Input value was saved successfully |  PASSED"

            outletCount += 1

        time.sleep(8)

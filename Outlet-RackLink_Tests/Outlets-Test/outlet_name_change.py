from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *
import time

class OutletNameChange(TestFixtures):
    def test_outlet_name(self):
        ipAddresses = get_ip_addresses()

        for ipAddress in ipAddresses:
            self.baseUrl = ipAddress

            ip_baseUrl_title(self.baseUrl)
            try:
                self.driver.get(self.baseUrl)
            except:
                print "Invalid IP Address"
                continue

            #self.outlet_name_check()
            self.outlet_name_blank()
            #self.outlet_name_length()

    # --------------------------------------------------------------

    def outlet_name_check(self):
        """
        Click on the outlet
        verify that the name has not changed after clicking the cancel btn.

        """
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletNameElement = '//div[8]/div[2]/input'

        randomInput = "Outlet Name"

        index = 2
        for outletBox in outletBoxList:
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

            driver.waitAndClick(cancel_btn_xpath(), XPATH)
            index += 1

        time.sleep(8)

    def outlet_name_blank(self):
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletNameElement = '//div[8]/div[2]/input'
        expectedOpGood = False

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()
            driver.waitForElement(outletNameElement, XPATH)
            driver.getElement(outletNameElement, XPATH).clear()

            driver.waitAndClick(save_btn_xpath(), XPATH)
            driver.getElement(outletNameElement, XPATH)

            outletNameElementClass = driver.getElementAttribute(outletNameElement, XPATH, ClASS)

            if 'has-error' in outletNameElementClass:
                expectedOpGood = True
                driver.waitAndClick("btnOk", ID)

            driver.waitAndClick(cancel_btn_xpath(), XPATH)

            assert expectedOpGood == True

        time.sleep(8)

    def outlet_name_length(self):
        """
        function to test outlets' name
        outlet name can only accept up to 50 characters (letters, digits, and special characters)

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletNameElement = '//div[8]/div[2]/input'

        # Random characters with a length of 50 to test outlet's name
        randomChars = 'g#QUfjeTakWbxHCS*6RQ579Wq6sBV3AT?#T!DrZ6#yJpbZzC$@'

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()
            driver.waitForElement(outletNameElement, XPATH)
            driver.sendInput(outletNameElement, XPATH, randomChars)

            driver.waitAndClick(save_btn_xpath(), XPATH)
            inputValue = driver.getElementAttribute(outletNameElement, XPATH, VALUE)

            #  assert input
            assert 50 >= len(inputValue) >= 1

        time.sleep(8)

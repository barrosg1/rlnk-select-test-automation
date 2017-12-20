import unittest
import time

from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *


class OutletNameChange(TestFixtures):

    #@unittest.skip("Skipped for now")
    def test_outlet_name_not_changed(self):
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
            driver.wait_until_clickable(outletNameElement, XPATH)
            driver.send_input(outletNameElement, XPATH, randomInput)

            driver.wait_and_click(outlet_cancel_btn(), XPATH)

            time.sleep(3)
            driver.wait_and_click(outletBoxStr, XPATH)

            driver.wait_until_clickable(outletNameElement, XPATH)
            driver.get_element(outletNameElement, XPATH)

            inputVal = driver.get_element_attribute(outletNameElement, XPATH, VALUE)

            assert inputVal != randomInput

            driver.wait_and_click(outlet_cancel_btn(), XPATH)
            index += 1

    #@unittest.skip("Skipped for now")
    def test_outlet_name_blank(self):
        """
        Verify that the name input box has a red border
        after changing the name to blank/empty

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletNameElement = '//div[8]/div[2]/input'

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()
            driver.wait_until_clickable(outletNameElement, XPATH)
            driver.get_element(outletNameElement, XPATH).clear()

            driver.wait_and_click(outlet_save_btn(), XPATH)

            assert self.is_hidden_string(notify_msg()) == False

            driver.wait_and_click("btnOk", ID)
            driver.wait_and_click(outlet_cancel_btn(), XPATH)

            assert self.has_error(outletNameElement) == True

    #@unittest.skip("Skipped for now")
    def test_outlet_name_length(self):
        """
        function to test outlets' name
        outlet name can only accept up to 50 characters (letters, digits, and special characters)

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletNameElement = '//div[8]/div[2]/input'

        # Random characters with a length of 50 to test outlet's name
        randomChars = 'g#QUfjeTakWbxHCS*6RQ579Wq6sBV3AT?#T!DrZ6#yJpbZzC$@'

        i = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(i)
            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)
            driver.wait_for_visibility(outletNameElement, XPATH)
            driver.send_input(outletNameElement, XPATH, randomChars)

            driver.wait_and_click(outlet_save_btn(), XPATH)

            time.sleep(2)
            if driver.is_element_present(close_btn_msg(), XPATH):
                assert self.is_hidden_string(success_msg()) == False
                driver.wait_and_click(close_btn_msg(), XPATH)

            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)
            inputValue = driver.get_element_attribute(outletNameElement, XPATH, VALUE)

            #  assert input
            assert 50 >= len(inputValue) >= 1

            driver.wait_and_click(outlet_cancel_btn(), XPATH)

            i += 1

        time.sleep(3)
        self.restore_outlet_defaults()

    # ---------------------------- Functions -----------------------------

    def restore_outlet_defaults(self):
        driver = SeleniumDriver(self.driver)
        factoryDefaults = "//nav/ul/li[5]"
        restore_outlet_def = "//*[@id='factoryDefaults']/p[3]/input"

        driver.wait_and_click(menu(), XPATH)
        time.sleep(3)
        driver.force_click(factoryDefaults, XPATH)

        time.sleep(3)

        driver.element_click(restore_outlet_def, XPATH)
        driver.wait_and_click(save_btn(), XPATH)

        time.sleep(11)  # wait for 10 seconds plus another second to click on OK button
        driver.element_click("btnOk", ID)

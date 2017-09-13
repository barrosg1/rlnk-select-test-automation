# coding=utf-8
import unittest
import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletRetries(TestFixtures):

    # @unittest.skip("Skipped for now")
    def test_verify_notify_msg_zero(self):
        """
        Verify that a warning notification appears letting you know the valid range of cycle delay values
        Verify that the input has a red border to show an error.

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        retries = 0

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()

            driver.send_input(retriesInputElem, XPATH, retries)
            driver.wait_and_click(outlet_save_btn(), XPATH)

            assert self.is_hidden_string(notify_msg()) == False

            driver.element_click("btnOk", ID)
            driver.element_click(outlet_cancel_btn(), XPATH)

            assert self.has_error(retriesInputElem) == True

    # @unittest.skip("Skipped for now")
    def test_verify_success_msg(self):
        """
        Verify that the Success message appears
        Verify that the outlet shrinks out edit mode and return to original location

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        outlet_div = "//div[8]"
        retries = 5

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()

            driver.send_input(retriesInputElem, XPATH, retries)
            driver.wait_and_click(outlet_save_btn(), XPATH)
            driver.wait_and_click(close_btn_msg(), XPATH)

            assert self.is_hidden_string(success_msg()) == False

            driver.wait_for_invisibility(outlet_div, XPATH)
            assert driver.is_element_present(outlet_div, XPATH) == False

    # @unittest.skip("Skipped for now")
    def test_verify_notify_msg_250(self):
        """
        Set the Retries to 250 and then click on the Save button.
        Verify that a warning notification appears
        Verify that the input has a red border to show an error.

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        retries = 250

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()

            driver.send_input(retriesInputElem, XPATH, retries)
            driver.wait_and_click(outlet_save_btn(), XPATH)

            assert self.is_hidden_string(notify_msg()) == False

            driver.element_click("btnOk", ID)
            driver.element_click(outlet_cancel_btn(), XPATH)

            assert self.has_error(retriesInputElem) == True

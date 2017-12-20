# coding=utf-8

import unittest
import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletFrequency(TestFixtures):

    #@unittest.skip("Skipped for now")
    def test_frequency_zero_input(self):
        """
        Set the Frequency to zero (0)
        Verify that a warning notification appears letting you know the valid range of cycle delay values
        Verify that the input has a red border to show an error.

        """
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        enableBtn = "//div[8]/div[2]/form[1]/button[2]"
        ip_addr_ping = "//div[8]/div[2]/form[2]/p[1]/input"
        frequency = 0

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()

            if not self.is_on(enableBtn):
                driver.wait_and_click(enableBtn, XPATH)

            driver.send_input(ip_addr_ping, XPATH, "8.8.8.8")
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.wait_and_click(outlet_save_btn(), XPATH)

            assert self.is_hidden_string(notify_msg()) == False

            driver.element_click("btnOk", ID)
            driver.element_click(outlet_cancel_btn(), XPATH)

            assert self.has_error(freqInputElem) == True

    #@unittest.skip("Skipped for now")
    def test_frequency_success_msg(self):
        """
        Verify that the Success message appears
        Verify that the outlet shrinks out edit mode and return to original location

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        ip_addr_ping = "//div[8]/div[2]/form[2]/p[1]/input"
        enableBtn = "//div[8]/div[2]/form[1]/button[2]"
        frequency = 30

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()

            if not self.is_on(enableBtn):
                driver.wait_and_click(enableBtn, XPATH)

            driver.send_input(ip_addr_ping, XPATH, "8.8.8.8")
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.wait_and_click(outlet_save_btn(), XPATH)

            time.sleep(2)
            if driver.is_element_present(close_btn_msg(), XPATH):
                assert self.is_hidden_string(success_msg()) == False
                driver.wait_and_click(close_btn_msg(), XPATH)

            time.sleep(1)
            assert driver.is_element_present("//div[8]", XPATH) == False

# coding=utf-8
import time

import unittest
from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletCycleDelay(TestFixtures):
    #@unittest.skip("Skipped for now")
    def test_cycle_invalid_input(self):
        """
        - Set the Cycle Delay to zero (0) and then click on the Start Cycle button
        - Verify that a warning notification appears letting
        you know the valid range of cycle delay values
        - Verify that the input has a red border to show an error

        """
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        cycleNum = 0  # cycle number in seconds
        cycleInput = '//div[8]/div[2]/form[1]/p[2]/input'
        startCycleBtn = "//div[8]/div[2]/form[1]/p[2]/button"

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            time.sleep(5)

            if self.is_on(outletCtrlStr) is False:
                index += 1
            else:
                outletBox.click()
                driver.wait_until_clickable(cycleInput, XPATH)
                driver.send_input(cycleInput, XPATH, cycleNum)

                driver.element_click(startCycleBtn, XPATH)

                assert self.is_hidden_string(notify_msg()) == False

                driver.element_click("btnOk", ID)

                assert self.has_error(cycleInput) == True
                driver.wait_and_click(outlet_cancel_btn(), XPATH)

    #@unittest.skip("Skipped for now")
    def test_outlet_cycle(self):
        """
        Verify that the cycle input is between 1 - 999
        Verify “Are you sure…” message appears
        Verify success message appears
        Verify that the outlet face has changed color
        Verify that the outlet shrinks out of edit mode

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        cycleNum = 10  # cycle number in seconds
        cycleInput = '//div[8]/div[2]/form[1]/p[2]/input'
        startCycleBtn = "//div[8]/div[2]/form[1]/p[2]/button"
        outletEditMode = "//div[8]"

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = "//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            time.sleep(5)

            outletBox.click()
            driver.wait_until_clickable(cycleInput, XPATH)
            driver.send_input(cycleInput, XPATH, cycleNum)

            # Verify that the cycle input is between 1 - 999
            cycleInputVal = driver.get_element_attribute(cycleInput, XPATH, VALUE)
            assert 1 <= int(cycleInputVal) <= 999

            driver.element_click(startCycleBtn, XPATH)

            # Verify “Are you sure…” message appears
            driver.wait_for_visibility(notify_msg(), XPATH)
            assert self.is_hidden_string(notify_msg()) == False

            driver.element_click("btnOk", ID)

            # Verify success message appears
            time.sleep(1)
            if driver.is_element_present(success_msg(), XPATH):
                assert self.is_hidden_string(success_msg()) == False

            # Verify that the outlet face has changed color to red
            time.sleep(5)
            driver.get_element(outletCtrlStr, XPATH)
            assert self.is_on(outletCtrlStr) == False

            # Verify that the outlet face has changed color to green
            time.sleep(cycleNum)
            driver.get_element(outletCtrlStr, XPATH)
            assert self.is_on(outletCtrlStr) == True

            # Verify that the outlet shrinks out of edit 0mode
            assert driver.is_element_present(outletEditMode, XPATH) == False

            index += 1

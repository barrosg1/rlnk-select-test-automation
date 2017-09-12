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

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            time.sleep(5)

            if self.is_off(outletCtrlStr):
                index += 1
            else:
                outlet_count(outletCount)
                outletBox.click()
                driver.wait_until_clickable(cycleInput, XPATH)
                driver.send_input(cycleInput, XPATH, cycleNum)

                driver.element_click(startCycleBtn, XPATH)

                assert self.is_hidden_string(notify_msg()) == False

                driver.element_click("btnOk", ID)

                assert self.has_error(cycleInput) == True
                driver.wait_and_click(outlet_cancel_btn(), XPATH)

                outletCount += 1

    @unittest.skip("Skipped for now")
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

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = "//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            time.sleep(5)

            outlet_count(outletCount)
            outletBox.click()
            driver.wait_until_clickable(cycleInput, XPATH)
            driver.send_input(cycleInput, XPATH, cycleNum)

            # Verify that the cycle input is between 1 - 999
            cycleInputVal = driver.get_element_attribute(cycleInput, XPATH, VALUE)
            assert 1 <= int(cycleInputVal) <= 999
            print "Input value is between 1 - 999 |  PASSED"

            driver.element_click(startCycleBtn, XPATH)

            # Verify “Are you sure…” message appears
            assert self.is_hidden_string(notify_msg()) == False
            print "Are you sure.. message appeared |  PASSED"

            driver.element_click("btnOk", ID)

            # Verify success message appears
            driver.wait_until_clickable("successMsg", ID)
            successMsg = driver.is_element_present("successMsg", ID)
            if successMsg:
                assert successMsg == True
                print "Success Message appeared |  PASSED"

            driver.wait_and_click(close_btn_msg(), XPATH)

            # Verify that the outlet face has changed color to red
            time.sleep(5)
            driver.get_element(outletCtrlStr, XPATH)
            assert self.is_off(outletCtrlStr) == True
            print "Outlet state is off for " + str(cycleNum) + " seconds |  PASSED"

            # Verify that the outlet face has changed color to green
            time.sleep(cycleNum)
            driver.get_element(outletCtrlStr, XPATH)
            assert self.is_off(outletCtrlStr) == False
            print "Outlet state changed back to on |  PASSED"
            
            # Verify that the outlet shrinks out of edit 0mode
            assert driver.is_element_present(outletEditMode, XPATH) == False
            print "Outlet shrunk out of edit mode | PASSED"

            outletCount += 1
            index += 1

            time.sleep(8)

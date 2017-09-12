# coding=utf-8
import sys
import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletRetries(TestFixtures):
    def test_outlet_power_state_change(self):
        self.verify_notify_msg_zero()
        self.verify_success_msg()
        self.verify_notify_msg_250()

    def verify_notify_msg_zero(self):
        """
        Verify that a warning notification appears letting you know the valid range of cycle delay values
        Verify that the input has a red border to show an error.

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        retries = 0

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()

            driver.send_input(retriesInputElem, XPATH, retries)
            driver.wait_and_click(outlet_save_btn(), XPATH)

            notifyVisible = driver.is_element_present(notify_msg(), XPATH)

            assert notifyVisible == True
            print "Notification message appeared |  PASSED"

            driver.element_click("btnOk", ID)
            driver.element_click(outlet_cancel_btn(), XPATH)

            retriesInputClass = driver.get_element_attribute(
                retriesInputElem, XPATH, ClASS)

            if 'has-error' in retriesInputClass:
                hasError = True
            else:
                hasError = False

            assert hasError == True
            print "Input box has a red border |  PASSED"

            outletCount += 1

        time.sleep(8)

    def verify_success_msg(self):
        """
        Verify that the Success message appears
        Verify that the outlet shrinks out edit mode and return to original location

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        retries = 5

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()

            driver.send_input(retriesInputElem, XPATH, retries)
            driver.wait_and_click(outlet_save_btn(), XPATH)

            successMsg = driver.is_element_present("successMsg", ID)
            assert successMsg == True
            print "Success message appeared |  PASSED"

            time.sleep(1)
            assert driver.is_element_present("//div[8]", XPATH) == False
            print "Outlet has shrunk out of edit mode | PASSED"

            outletCount += 1

        time.sleep(5)

    def verify_notify_msg_250(self):
        """
        Set the Retries to 250 and then click on the Save button.
        Verify that a warning notification appears
        Verify that the input has a red border to show an error.

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        retries = 250

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()

            driver.send_input(retriesInputElem, XPATH, retries)
            driver.wait_and_click(outlet_save_btn(), XPATH)

            notifyVisible = driver.is_element_present(notify_msg(), XPATH)

            assert notifyVisible == True
            print "Notification message appeared |  PASSED"

            driver.element_click("btnOk", ID)
            driver.element_click(outlet_cancel_btn(), XPATH)

            retriesInputClass = driver.get_element_attribute(
                retriesInputElem, XPATH, ClASS)

            if 'has-error' in retriesInputClass:
                hasError = True
            else:
                hasError = False

            assert hasError == True
            print "Input box has a red border |  PASSED"

            outletCount += 1

        time.sleep(8)

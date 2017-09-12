# coding=utf-8
import sys
import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletPowerState(TestFixtures):
    def test_outlet_power_state_change(self):
        self.power_state_btn_notify_msg()
        self.power_state_verify_not_changed()
        self.power_state_verify_changed()

    def power_state_btn_notify_msg(self):
        """
        Verifies that a popup comes up with an Are you sure… message.
        Look for the DOM element “notify”

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerStateBtn = '//div[8]/div[2]/form[1]/button[1]'

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()
            driver.wait_and_click(powerStateBtn, XPATH)

            notifyMsg = driver.is_element_present(notify_msg(), XPATH)

            assert notifyMsg == True
            print '"Are you sure.." message appeared |  PASSED'

            driver.wait_and_click("btnOk", ID)

            outletCount += 1

        time.sleep(8)

    def power_state_verify_not_changed(self):
        """
        Verify that the power state has not changed
        after clicking the cancel button

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerStateBtn = '//div[8]/div[2]/form[1]/button[1]'

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()
            powerStateBtnClass = driver.get_element_attribute(powerStateBtn, XPATH, ClASS)

            if 'state1' in powerStateBtnClass:
                powerState = True
            else:
                powerState = False

            driver.wait_and_click(powerStateBtn, XPATH)
            driver.wait_and_click("btnCancel", ID)
            driver.wait_and_click(outlet_cancel_btn(), XPATH)

            if powerState:
                print "Power state has not changed |  PASSED"
                assert powerState == True

            if 'state2' in powerStateBtnClass:
                print "Power state has not changed |  PASSED"
                assert powerState == False

            outletCount += 1

        time.sleep(8)

    def power_state_verify_changed(self):
        """
        Verify that the switch and outlet face change state
        Verify that a success message appears
        Verify that the outlet shrinks out of edit mode

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerStateBtn = '//div[8]/div[2]/form[1]/button[1]'
        outletEditMode = "//div[8]"

        index = 2
        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            time.sleep(5)
            outletBox.click()

            powerStateBtnClass = driver.get_element_attribute(powerStateBtn, XPATH, ClASS)

            if 'state1' in powerStateBtnClass:
                powerState = True
            else:
                powerState = False

            driver.wait_and_click(powerStateBtn, XPATH)
            driver.wait_and_click("btnOk", ID)

            successMsg = driver.is_element_present("successMsg", ID)
            assert successMsg == True
            print "Success message appeared |  PASSED"

            time.sleep(1)

            assert driver.is_element_present(outletEditMode, XPATH) == False
            print "Outlet shrunk out of edit mode | PASSED"

            driver.element_click(outletCtrlStr, XPATH)

            powerStateBtnClass = driver.get_element_attribute(powerStateBtn, XPATH, ClASS)

            if powerState:
                if 'state1' not in powerStateBtnClass:
                    print "Power state changed to red |  PASSED"
                    assert powerState == True
            else:
                print "Power changed to green |  PASSED"
                assert powerState == False

            driver.wait_and_click(outlet_cancel_btn(), XPATH)

            index += 1
            outletCount += 1

        time.sleep(8)

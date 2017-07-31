# coding=utf-8
from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *
import sys
import time


class OutletPowerState(TestFixtures):
    def test_outlet_power_state_change(self):
        ipAddresses = get_ip_addresses()
        for ipAddress in ipAddresses:
            self.baseUrl = ipAddress

            ip_baseUrl_title(self.baseUrl)
            try:
                self.driver.get(self.baseUrl)
            except:
                print "Invalid IP Address"
                continue

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
        notify = ".//*[@id='notify']/div"

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()
            driver.waitAndClick(powerStateBtn, XPATH)

            notifyMsg = driver.isElementPresent(notify, XPATH)

            assert notifyMsg == True
            print '"Are you sure.." message appeared |  PASSED'

            driver.waitAndClick("btnOk", ID)

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
            powerStateBtnClass = driver.getElementAttribute(powerStateBtn, XPATH, ClASS)

            if 'state1' in powerStateBtnClass:
                powerState = True
            else:
                powerState = False

            driver.waitAndClick(powerStateBtn, XPATH)
            driver.waitAndClick("btnCancel", ID)
            driver.waitAndClick(cancel_btn_xpath(), XPATH)

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

            powerStateBtnClass = driver.getElementAttribute(powerStateBtn, XPATH, ClASS)

            if 'state1' in powerStateBtnClass:
                powerState = True
            else:
                powerState = False

            driver.waitAndClick(powerStateBtn, XPATH)
            driver.waitAndClick("btnOk", ID)

            successMsg = driver.isElementPresent("successMsg", ID)
            assert successMsg == True
            print "Success message appeared |  PASSED"

            time.sleep(1)

            assert driver.isElementPresent(outletEditMode, XPATH) == False
            print "Outlet shrunk out of edit mode | PASSED"

            driver.elementClick(outletCtrlStr, XPATH)

            powerStateBtnClass = driver.getElementAttribute(powerStateBtn, XPATH, ClASS)

            if powerState:
                if 'state1' not in powerStateBtnClass:
                    print "Power state changed to red |  PASSED"
                    assert powerState == True
            else:
                print "Power changed to green |  PASSED"
                assert powerState == False

            driver.waitAndClick(cancel_btn_xpath(), XPATH)

            index += 1
            outletCount += 1

        time.sleep(8)

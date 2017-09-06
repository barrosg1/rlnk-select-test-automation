# coding=utf-8
import sys
import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletCycleDelay(TestFixtures):
    def test_outlet_cycle_delay(self):
        self.cycle_invalid_input()
        self.outlet_cycle()

    def cycle_invalid_input(self):
        """
        - Set the Cycle Delay to zero (0) and then click on the Start Cycle button
        - Verify that a warning notification appears letting
        you know the valid range of cycle delay values
        - Verify that the input has a red border to show an error

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        cycleNum = 0  # cycle number in seconds
        cycleInput = '//div[8]/div[2]/form[1]/p[2]/input'
        notifyMsg = ".//*[@id='notify']"
        startCycleBtn = "//div[8]/div[2]/form[1]/p[2]/button"

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            outletCtrlClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            time.sleep(5)

            if 'state-off' in outletCtrlClass:
                index += 1
            else:
                outlet_count(outletCount)
                outletBox.click()
                driver.waitUntilClickable(cycleInput, XPATH)
                driver.sendInput(cycleInput, XPATH, cycleNum)

                driver.elementClick(startCycleBtn, XPATH)

                notifyMsgClass = driver.getElementAttribute(notifyMsg, XPATH, ClASS)
                if 'hidden' not in notifyMsgClass:
                    notifyShowed = True
                    print "Warning notification message appeared |  PASSED"
                else:
                    notifyShowed = False

                assert notifyShowed == True

                driver.elementClick("btnOk", ID)

                cycleInputClass = driver.getElementAttribute(cycleInput, XPATH, ClASS)

                if 'has-error' in cycleInputClass:
                    hasError = True
                    print "Input box has a red border |  PASSED"
                else:
                    hasError = False

                assert hasError == True

                driver.waitAndClick(cancel_btn_xpath(), XPATH)

                outletCount += 1

    def outlet_cycle(self):
        """
        Verify that the cycle input is between 1 - 999
        Verify “Are you sure…” message appears
        Verify success message appears
        Verify that the outlet face has changed color
        Verify that the outlet shrinks out of edit mode

        """

        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        cycleNum = 10  # cycle number in seconds
        cycleInput = '//div[8]/div[2]/form[1]/p[2]/input'
        startCycleBtn = "//div[8]/div[2]/form[1]/p[2]/button"
        notifyMsg = "//*[@id='notify']"
        outletEditMode = "//div[8]"

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = "//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            time.sleep(5)

            outlet_count(outletCount)
            outletBox.click()
            driver.waitUntilClickable(cycleInput, XPATH)
            driver.sendInput(cycleInput, XPATH, cycleNum)

            # Verify that the cycle input is between 1 - 999
            cycleInputVal = driver.getElementAttribute(cycleInput, XPATH, VALUE)
            assert 1 <= int(cycleInputVal) <= 999
            print "Input value is between 1 - 999 |  PASSED"

            driver.elementClick(startCycleBtn, XPATH)

            # Verify “Are you sure…” message appears
            notifyMsgClass = driver.getElementAttribute(notifyMsg, XPATH, ClASS)
            if 'hidden' not in notifyMsgClass:
                notifyShowed = True
            else:
                notifyShowed = False

            assert notifyShowed == True
            print "Are you sure.. message appeared |  PASSED"

            driver.elementClick("btnOk", ID)

            # Verify success message appears
            driver.waitUntilClickable("successMsg", ID)
            successMsg = driver.isElementPresent("successMsg", ID)
            if successMsg:
                assert successMsg == True
                print "Success Message appeared |  PASSED"

            driver.waitAndClick(close_btn_msg(), XPATH)

            # Verify that the outlet face has changed color
            time.sleep(5)
            driver.getElement(outletCtrlStr, XPATH)
            outletCtrlClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            if 'state-off' in outletCtrlClass:
                state = False
            else:
                state = True

            assert state == False
            print "Outlet state is off for " + str(cycleNum) + " seconds |  PASSED"

            time.sleep(cycleNum)
            driver.getElement(outletCtrlStr, XPATH)
            outletCtrlClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletCtrlClass:
                state = True
            else:
                state = False
            assert state == True
            print "Outlet state changed back to on |  PASSED"
            
            # Verify that the outlet shrinks out of edit 0mode
            assert driver.isElementPresent(outletEditMode, XPATH) == False
            print "Outlet shrunk out of edit mode | PASSED"

            outletCount += 1
            index += 1

            time.sleep(8)

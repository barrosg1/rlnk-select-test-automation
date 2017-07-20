# coding=utf-8
from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *
from selenium.common.exceptions import *
import time


class OutletCycleDelay(TestFixtures):
    def test_outlet_cycle_delay(self):
        ipAddresses = get_ip_addresses()
        for ipAddress in ipAddresses:
            self.baseUrl = ipAddress

            ip_baseUrl_title(self.baseUrl)
            try:
                self.driver.get(self.baseUrl)
            except:
                print "Invalid IP Address"
                continue

            # self.cycle_invalid_input()
            self.outlet_cycle()

    # ------------------------------------------------------------

    def cycle_invalid_input(self):
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
                print "\n::::: Outlet " + str(outletCount) + " :::::\n"
                outletBox.click()
                driver.waitForElement(cycleInput, XPATH)
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

                outletCount += 1

    def outlet_cycle(self):
        """
        Verify that the cycle input is between 1 - 999
        Verify that you get the “Are you sure…” message
        Verify success message appears
        verify the corresponding light went off
        Verify that the outlet shrinks out of editmode

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        cycleNum = 10  # cycle number in seconds
        cycleInput = '//div[8]/div[2]/form[1]/p[2]/input'
        startCycleBtn = "//div[8]/div[2]/form[1]/p[2]/button"
        notifyMsg = ".//*[@id='notify']"

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            outletCtrlClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            time.sleep(5)

            if 'state-off' in outletCtrlClass:
                index += 1
            else:
                print "\n::::: Outlet " + str(outletCount) + " :::::\n"
                outletBox.click()
                driver.waitForElement(cycleInput, XPATH)
                driver.sendInput(cycleInput, XPATH, cycleNum)

                cycleInputVal = driver.getElementAttribute(cycleInput, XPATH, VALUE)

                assert 1 <= int(cycleInputVal) <= 999
                print "Input value is between 1 - 999 |  PASSED"

                driver.elementClick(startCycleBtn, XPATH)

                notifyMsgClass = driver.getElementAttribute(notifyMsg, XPATH, ClASS)
                if 'hidden' not in notifyMsgClass:
                    notifyShowed = True
                    print "Are you sure.. message appeared |  PASSED"
                else:
                    notifyShowed = False

                assert notifyShowed == True

                driver.elementClick("btnOk", ID)

                driver.waitForElement("successMsg", ID)
                successMsg = driver.isElementPresent("successMsg", ID)

                if successMsg:
                    assert successMsg == True
                    print "Success Message appeared |  PASSED"

                driver.waitAndClick(".//*[@id='closeBtn6']/span", XPATH)

                time.sleep(3)
                driver.waitForElement(outletCtrlStr, XPATH)
                driver.getElement(outletCtrlStr, XPATH)
                print driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)

                time.sleep(cycleNum-3)
                driver.waitForElement(outletCtrlStr, XPATH)
                driver.getElement(outletCtrlStr, XPATH)
                print driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)

            outletCount += 1

        time.sleep(cycleNum)

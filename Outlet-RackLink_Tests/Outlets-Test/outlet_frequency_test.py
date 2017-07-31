# coding=utf-8
from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *
import sys
import time


class OutletFrequency(TestFixtures):
    def test_outlet_frequency(self):
        ipAddresses = get_ip_addresses()
        for ipAddress in ipAddresses:
            self.baseUrl = ipAddress

            ip_baseUrl_title(self.baseUrl)
            try:
                self.driver.get(self.baseUrl)
            except:
                print "Invalid IP Address"
                continue

            self.frequency_zero_input()
            print "\n--------------------------------------------\n"
            self.frequency_success_msg()

    def frequency_zero_input(self):
        """
        Set the Frequency to zero (0)
        Verify that a warning notification appears letting you know the valid range of cycle delay values
        Verify that the input has a red border to show an error.

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        notify = ".//*[@id='notify']"
        frequency = 0

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()

            driver.sendInput(freqInputElem, XPATH, frequency)
            driver.waitAndClick(outlet_save_btn(), XPATH)

            notifyVisible = driver.isElementPresent(notify, XPATH)

            assert notifyVisible == True
            print "Notification message appeared |  PASSED"

            driver.elementClick("btnOk", ID)
            driver.elementClick(cancel_btn_xpath(), XPATH)

            freqInputClass = driver.getElementAttribute(
                freqInputElem, XPATH, ClASS)

            if 'has-error' in freqInputClass:
                print "Input box has a red border |  PASSED"
                hasError = True
            else:
                hasError = False

            assert hasError == True

            outletCount += 1

        time.sleep(8)

    def frequency_success_msg(self):
        """
        Verify that the Success message appears
        Verify that the outlet shrinks out edit mode and return to original location

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        frequency = 30

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()

            driver.sendInput(freqInputElem, XPATH, frequency)
            driver.waitAndClick(outlet_save_btn(), XPATH)

            successMsg = driver.isElementPresent("successMsg", ID)
            assert successMsg == True
            print "Success message appeared |  PASSED"

            time.sleep(1)
            assert driver.isElementPresent("//div[8]", XPATH) == False
            print "Outlet has shrunk out of edit mode | PASSED"

            outletCount += 1

        time.sleep(5)

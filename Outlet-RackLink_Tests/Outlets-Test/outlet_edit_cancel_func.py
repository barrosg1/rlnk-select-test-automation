# coding=utf-8
from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *
import sys
import time


class OutletEditCancel(TestFixtures):
    def test_outlet_edit_cancel(self):
        ipAddresses = get_ip_addresses()
        for ipAddress in ipAddresses:
            self.baseUrl = ipAddress

            ip_baseUrl_title(self.baseUrl)
            try:
                self.driver.get(self.baseUrl)
            except:
                print "Invalid IP Address"
                continue

            self.edit_cancel_btn()

    def edit_cancel_btn(self):
        """
        Verification of Outlet Edit mode and Cancel Button Functionality
        verify that the outlet has the “guitarSolo” class
        verify that the outlet no longer has the “guitarSolo” class

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletEditMode = "//div[8]"

        index = 2
        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            expectedOpGood = True
            time.sleep(5)
            outletBox.click()

            outletElemClass = driver.getElementAttribute(outletEditMode, XPATH, ClASS)

            if 'guitarSolo' in outletElemClass:
                print "Outlet expands into edit mode | PASSED"
                assert expectedOpGood == True

            driver.waitAndClick(cancel_btn_xpath(), XPATH)

            time.sleep(1)
            assert driver.isElementPresent(outletEditMode, XPATH) == False
            print "Outlet shrunk out of edit mode | PASSED"

            index += 1
            outletCount += 1
        time.sleep(8)

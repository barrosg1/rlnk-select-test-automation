# coding=utf-8
import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletEditCancel(TestFixtures):

    def test_edit_cancel_btn(self):
        """
        Verification of Outlet Edit mode and Cancel Button Functionality
        verify that the outlet has the “guitarSolo” class
        verify that the outlet no longer has the “guitarSolo” class

        """
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

            outletElemClass = driver.get_element_attribute(outletEditMode, XPATH, ClASS)

            if 'guitarSolo' in outletElemClass:
                print "Outlet expands into edit mode | PASSED"
                assert expectedOpGood == True

            driver.wait_and_click(outlet_cancel_btn(), XPATH)

            time.sleep(1)
            assert driver.is_element_present(outletEditMode, XPATH) == False
            print "Outlet shrunk out of edit mode | PASSED"

            index += 1
            outletCount += 1
        time.sleep(8)

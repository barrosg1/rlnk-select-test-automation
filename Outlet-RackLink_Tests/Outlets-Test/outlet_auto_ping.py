import sys
import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletAutoPing(TestFixtures):
    def test_outlet_auto_ping(self):
        pass

    def autoPing_enable(self):
        """
        Asserts if the enable button is on/off

        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        enabledBtn = '//div[8]/div[2]/form[1]/button[2]'

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()

            enabledBtnClass = driver.getElement(enabledBtn, XPATH).get_attribute(ClASS)

            if 'state1' in enabledBtnClass:
                driver.waitAndClick(enabledBtn, XPATH)
            else:
                state = False
                assert state == True

            driver.waitAndClick(outlet_save_btn(), XPATH)
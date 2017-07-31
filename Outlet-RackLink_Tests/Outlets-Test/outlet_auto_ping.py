from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *
import sys
import time


class OutletAutoPing(TestFixtures):
    def test_outlet_auto_ping(self):
        ipAddresses = get_ip_addresses()
        for ipAddress in ipAddresses:
            self.baseUrl = ipAddress

            ip_baseUrl_title(self.baseUrl)
            try:
                self.driver.get(self.baseUrl)
            except:
                print "Invalid IP Address"
                continue

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
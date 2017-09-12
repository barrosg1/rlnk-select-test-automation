import sys
import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletAutoPing(TestFixtures):
    def test_autoPing_enable(self):
        """
        Asserts if the enable button is on/off

        """
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        enabledBtn = '//div[8]/div[2]/form[1]/button[1]'
        status_log = "//*[@id='group1']/div[2]"
        close_status_log = "//*[@id='closeBtn2']/span"

        i = 2
        for outlet in outletBoxList:
            outlet_status = "//*[@id='eventDisplay']/span[{0}]/span[1]".format(i)
            outlet = "//*[@id='outletControl']/div[{0}]".format(i)
            time.sleep(5)
            driver.wait_and_click(outlet, XPATH)

            driver.wait_and_click(enabledBtn, XPATH)
            driver.wait_and_click("btnOk", ID)
            driver.wait_and_click(close_btn_msg(), XPATH)

            self.driver.refresh()
            driver.wait_and_click(status_log, XPATH)

            outlet_status_class = driver.get_element_attribute(outlet_status, XPATH, ClASS)

            if "state-off" in outlet_status_class:
                state_off = True
            else:
                state_off = False

            assert state_off == True

            time.sleep(3)
            driver.wait_and_click(close_status_log, XPATH)

            i += 1

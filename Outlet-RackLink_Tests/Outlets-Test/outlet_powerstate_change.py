# coding=utf-8
from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *
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
        Look for the DOM element with the id of “notify”

        """
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerStateBtn = '//div[8]/div[2]/form[1]/button[1]'
        notify = ".//*[@id='notify']/div"

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()
            driver.waitAndClick(powerStateBtn, XPATH)

            notifyMsg = driver.isElementPresent(notify, XPATH)

            assert notifyMsg == True

            driver.waitAndClick("btnOk", ID)
            driver.waitAndClick(cancel_btn_xpath(), XPATH)

        time.sleep(8)

    def power_state_verify_not_changed(self):
        """
        Verifies that a popup comes up with an Are you sure… message.
        Look for the DOM element with the id of “notify”

        """
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerStateBtn = '//div[8]/div[2]/form[1]/button[1]'

        index = 1
        for outletBox in outletBoxList:
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
                print "Outlet " + str(index) + " | Power state has not changed: PASSED"
                assert powerState == True

            if 'state2' in powerStateBtnClass:
                print "Outlet " + str(index) + " | Power state has not changed: PASSED"
                assert powerState == False

            index += 1

        time.sleep(8)

    def power_state_verify_changed(self):
        """
        Verify that the switch and outlet face change state
        Verify that the outlet shrinks down and a success message appears
        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerStateBtn = '//div[8]/div[2]/form[1]/button[1]'

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()
            driver.waitAndClick(powerStateBtn, XPATH)
            driver.waitAndClick("btnOk", ID)

            driver.waitForElement("successMsg", ID)
            successMsg = driver.isElementPresent("successMsg", ID)

            assert successMsg == True

        time.sleep(8)

# coding=utf-8
import sys
import time

import unittest
from selenium import webdriver
from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from selenium.webdriver.common.keys import Keys
from Utils.string_constants import *
from Utils.test_operation import *

# global variables
enableBtn = "//div[8]/div[2]/form[1]/button[2]"
outletFace = "//div[8]/div[1]"
stateBtn = "//div[8]/div[2]/form[1]/button[1]"


class OutletRecoveryAction(TestFixtures):

    #@unittest.skip("Skipped for now")
    def test_power_off(self):
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerOffOption = "//div[8]/div[2]/form[2]/select/option[contains(@value, '1')]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        frequency = 30
        retries = 2
        waitTime = (frequency * retries) * 2

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)

            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            if not self.is_on(outletFace):
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                driver.wait_and_click(close_btn_msg(), XPATH)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

            if not self.is_on(enableBtn):
                driver.wait_and_click(enableBtn, XPATH)

            # input for ip address to ping, frequency, and retries
            time.sleep(3)
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            time.sleep(3)
            driver.wait_and_click(selectOptions, XPATH)

            if driver.is_element_selected(powerOffOption, XPATH):
                driver.wait_and_click(outlet_save_btn(), XPATH)
            else:
                driver.wait_and_click(powerOffOption, XPATH)
                self.driver.find_element_by_xpath(powerOffOption).send_keys(Keys.ENTER)
                driver.wait_and_click(outlet_save_btn(), XPATH)

            # in case the notification message to confirm changes pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify_msg()).is_displayed()
            if notifyDisplayed:
                driver.element_click("btnOk", ID)

            # verify if "AutoPing Failed" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Failed', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Replied', waitTime)
            driver.get_element(autoPingTitle, XPATH)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.get_element(outletCtrlStr, XPATH)
            driver.element_click(outletCtrlStr, XPATH)
            driver.wait_and_click(stateBtn, XPATH)
            driver.element_click("btnOk", ID)

            time.sleep(1)
            if driver.is_element_present(close_btn_msg(), XPATH):
                driver.element_click(close_btn_msg(), XPATH)
            else:
                time.sleep(3)

            time.sleep(3)
            self.change_ip_address_to_default(outletCtrlStr, ipAddressInputElem)

            index += 1

    @unittest.skip("Skipped for now")
    def test_power_off_pending_recovery(self):
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerOffPendRec = "//div[8]/div[2]/form[2]/select/option[contains(@value, '2')]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        frequency = 30
        retries = 2
        waitTime = (frequency * retries) * 2

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)

            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            if not self.is_on(outletFace):
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

            if not self.is_on(enableBtn):
                driver.wait_and_click(enableBtn, XPATH)

            # input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            time.sleep(3)
            driver.wait_and_click(selectOptions, XPATH)

            if driver.is_element_selected(powerOffPendRec, XPATH):
                driver.wait_and_click(outlet_save_btn(), XPATH)
            else:
                driver.wait_and_click(powerOffPendRec, XPATH)
                self.driver.find_element_by_xpath(powerOffPendRec).send_keys(Keys.ENTER)
                driver.wait_and_click(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify_msg()).is_displayed()
            if notifyDisplayed:
                driver.element_click("btnOk", ID)

            # verify if "AutoPing Failed" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Failed', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Replied', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Replied"

            # verify that the outlet in the UUT turned back on
            assert self.is_on(outletCtrlStr) == True

            # open outlet in UUT, change ip address to default, & save changes
            time.sleep(3)
            self.change_ip_address_to_default(outletCtrlStr, ipAddressInputElem)

            index += 1

    @unittest.skip("Skipped for now")
    def test_power_on(self):

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerOn = "//div[8]/div[2]/form[2]/select/option[contains(@value, '3')]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        frequency = 30
        retries = 2
        waitTime = (frequency * retries) * 2

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)

            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            if self.is_on(outletFace):
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                driver.wait_and_click(close_btn_msg(), XPATH)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

            if not self.is_on(enableBtn):
                driver.wait_and_click(enableBtn, XPATH)

            # input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            time.sleep(3)
            driver.wait_and_click(selectOptions, XPATH)

            if driver.is_element_selected(powerOn, XPATH):
                driver.wait_and_click(outlet_save_btn(), XPATH)
            else:
                driver.wait_and_click(powerOn, XPATH)
                self.driver.find_element_by_xpath(powerOn).send_keys(Keys.ENTER)
                driver.wait_and_click(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify_msg()).is_displayed()
            if notifyDisplayed:
                driver.element_click("btnOk", ID)

            # verify if "AutoPing Failed" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Failed', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Failed"

            # verify that the outlet in the UUT turned on
            assert self.is_on(outletCtrlStr) == True

            self.ctrl_device_power()  # turn outlet back on in the control device

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Replied', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Replied"

            # verify that the outlet in the UUT turned back on
            assert self.is_on(outletCtrlStr) == True

            # open outlet in UUT, change ip address to default, & save changes
            time.sleep(3)
            self.change_ip_address_to_default(outletCtrlStr, ipAddressInputElem)

            index += 1

    @unittest.skip("Skipped for now")
    def test_power_on_pending_recovery(self):

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerOnPendRec = "//div[8]/div[2]/form[2]/select/option[contains(@value, '4')]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        frequency = 30
        retries = 2
        waitTime = (frequency * retries) * 2

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            outletOn = "//*[@id='outletControl']/div[{0}]/div[contains(@class, 'state-on')]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)

            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            if self.is_on(outletFace):
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                driver.wait_and_click(close_btn_msg(), XPATH)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

            if not self.is_on(enableBtn):
                driver.wait_and_click(enableBtn, XPATH)

            # input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            time.sleep(3)
            driver.wait_and_click(selectOptions, XPATH)

            if driver.is_element_selected(powerOnPendRec, XPATH):
                driver.wait_and_click(outlet_save_btn(), XPATH)
            else:
                driver.wait_and_click(powerOnPendRec, XPATH)
                self.driver.find_element_by_xpath(powerOnPendRec).send_keys(Keys.ENTER)
                driver.wait_and_click(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify_msg()).is_displayed()
            if notifyDisplayed:
                driver.element_click("btnOk", ID)

            # verify if "AutoPing Failed" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Failed', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            # verify that the outlet in the UUT turned on
            driver.wait_for_visibility(outletOn, XPATH)
            assert self.is_on(outletCtrlStr) == True

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Replied', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, change ip address to default, & save changes
            time.sleep(3)
            self.change_ip_address_to_default(outletCtrlStr, ipAddressInputElem)

            if not self.is_on(outletCtrlStr):
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)
                driver.wait_and_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                driver.wait_and_click(close_btn_msg(), XPATH)

            index += 1

    @unittest.skip("Skipped for now")
    def test_power_cycle_once(self):
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerCycleOnce = "//div[8]/div[2]/form[2]/select/option[contains(@value, '5')]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        cycleDelayElem = "//div[8]/div[2]/form[2]/p[6]/input"
        frequency = 30
        retries = 2
        cycleDelay = 3
        waitTime = (frequency * retries) * 2

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)

            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            if not self.is_on(outletFace):
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                driver.wait_and_click(close_btn_msg(), XPATH)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

            if not self.is_on(enableBtn):
                driver.wait_and_click(enableBtn, XPATH)

            # send input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            time.sleep(3)
            driver.wait_and_click(selectOptions, XPATH)

            if driver.is_element_selected(powerCycleOnce, XPATH):
                driver.wait_and_click(outlet_save_btn(), XPATH)
            else:
                driver.wait_and_click(powerCycleOnce, XPATH)
                self.driver.find_element_by_xpath(powerCycleOnce).send_keys(Keys.ENTER)
                driver.wait_until_clickable(cycleDelayElem, XPATH)
                driver.send_input(cycleDelayElem, XPATH, cycleDelay)
                driver.wait_and_click(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify_msg()).is_displayed()
            if notifyDisplayed:
                driver.element_click("btnOk", ID)

            # verify if "AutoPing Failed" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Failed', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            # verify that the outlet in the UUT turned back on
            assert self.is_on(outletCtrlStr) == True

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Replied', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            self.change_ip_address_to_default(outletCtrlStr, ipAddressInputElem)

            index += 1

    @unittest.skip("Skipped for now")
    def test_power_cycle_until_recovery(self):

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerCycUntilRec = "//div[8]/div[2]/form[2]/select/option[contains(@value, '6')]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        cycleDelayElem = "//div[8]/div[2]/form[2]/p[6]/input"
        frequency = 30
        retries = 2
        cycleDelay = 3
        waitTime = (frequency * retries) * 2

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            outletOn = "//*[@id='outletControl']/div[{0}]/div[contains(@class, 'state-on')]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)

            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            if self.is_on(outletFace) is False:
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                driver.wait_and_click(close_btn_msg(), XPATH)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

            if not self.is_on(enableBtn):
                driver.wait_and_click(enableBtn, XPATH)

            # input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            time.sleep(3)
            driver.wait_and_click(selectOptions, XPATH)

            if driver.is_element_selected(powerCycUntilRec, XPATH):
                driver.wait_and_click(outlet_save_btn(), XPATH)
            else:
                driver.wait_and_click(powerCycUntilRec, XPATH)
                self.driver.find_element_by_xpath(powerCycUntilRec).send_keys(Keys.ENTER)
                driver.wait_until_clickable(cycleDelayElem, XPATH)
                driver.send_input(cycleDelayElem, XPATH, cycleDelay)
                driver.wait_and_click(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify_msg()).is_displayed()
            if notifyDisplayed:
                driver.element_click("btnOk", ID)

            # verify if "AutoPing Failed" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Failed', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            # verify that the outlet in the UUT is on, wait cycle delay
            # then verify that the outlet turned off
            driver.wait_for_visibility(outletOn, XPATH)
            assert self.is_on(outletCtrlStr) == True
            time.sleep(cycleDelay+1)
            assert self.is_on(outletCtrlStr) == False

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            driver.wait_text_to_be_present_in_elem(autoPingTitle, XPATH, 'AutoPing Replied', waitTime)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            self.change_ip_address_to_default(outletCtrlStr, ipAddressInputElem)

            index += 1

    # ----------------------------------- Functions --------------------------------------

    def ctrl_device_power(self):
        """
        This function opens the control device url to turn on/off the
         third outlet (RLNK-915R) to test UUT auto ping response

        """
        outlet3 = "//*[@id='outletControl']/div[4]"
        stateBtn = "html/body/div[8]/div[2]/form[1]/button[1]"

        self.ctrlDriver = webdriver.Firefox()
        self.ctrlDriver.implicitly_wait(10)

        ipAddress = get_ip_addresses()
        self.ctrlUrl = ipAddress[1]  # control device url
        try:
            self.ctrlDriver.get(self.ctrlUrl)
        except:
            print "Invalid IP Address"

        ctrlDriver = SeleniumDriver(self.ctrlDriver)
        ctrlDriver.element_click(outlet3, XPATH)

        # turn outlet off and close success message alert
        time.sleep(3)
        ctrlDriver.wait_and_click(stateBtn, XPATH)
        ctrlDriver.wait_and_click("btnOk", ID)
        ctrlDriver.wait_and_click(close_btn_msg(), XPATH)

        time.sleep(3)
        self.ctrlDriver.quit()

    def change_ip_address_to_default(self, outletCtrlStr, ipAddressInputElem):
        driver = SeleniumDriver(self.driver)
        driver.get_element(outletCtrlStr, XPATH)
        driver.wait_and_click(outletCtrlStr, XPATH)
        driver.send_input(ipAddressInputElem, XPATH, "8.8.8.8")
        driver.wait_and_click(outlet_save_btn(), XPATH)

        time.sleep(1)
        if driver.is_element_present(success_msg(), XPATH):
            driver.wait_and_click(close_btn_msg(), XPATH)
        else:
            time.sleep(3)

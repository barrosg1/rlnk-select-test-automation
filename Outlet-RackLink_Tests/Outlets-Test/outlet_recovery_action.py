# coding=utf-8
import sys
import time

import unittest
from selenium import webdriver
from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from Utils.string_constants import *
from Utils.test_operation import *


class OutletRecoveryAction(TestFixtures):

    # @unittest.skip("Skipped for now")
    def test_power_off(self):
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerOffOption = "//div[8]/div[2]/form[2]/select/option[contains(@value, '1')]"
        outletFace = "//div[8]/div[1]"
        stateBtn = "//div[8]/div[2]/form[1]/button[1]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        frequency = 30
        retries = 2
        waitTime = frequency * retries

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)
            apr = ".//*[@id='outletControl']/div[{0}]/h6[contains(text(), 'AutoPing Replied')]".format(
                index)  # AutoPing Replied title
            apf = ".//*[@id='outletControl']/div[{0}]/h6[contains(text(), 'AutoPing Failed')]".format(
                index)  # AutoPing Failed title
            wait = WebDriverWait(self.driver, waitTime)

            outlet_count(outletCount)

            time.sleep(5)
            outletBox.click()

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            # input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            if self.is_on(outletFace) is False:
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

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
            driver.wait_for_visibility(apf, XPATH)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            wait.until(EC.presence_of_element_located((By.XPATH, apr)))
            driver.get_element(autoPingTitle, XPATH)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.get_element(outletCtrlStr, XPATH)
            driver.element_click(outletCtrlStr, XPATH)
            driver.wait_and_click(stateBtn, XPATH)
            driver.element_click("btnOk", ID)
            time.sleep(5)
            self.change_ip_address_to_default(outletCtrlStr, ipAddressInputElem)

            time.sleep(5)
            outletCount += 1
            index += 1

    @unittest.skip("Skipped for now")
    def test_power_off_pending_recovery(self):
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerOffPendRec = "//div[8]/div[2]/form[2]/select/option[contains(@value, '2')]"
        outletFace = "//div[8]/div[1]"
        stateBtn = "//div[8]/div[2]/form[1]/button[1]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        frequency = 30
        retries = 2
        waitTime = frequency * retries

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)
            apr = ".//*[@id='outletControl']/div[{0}]/h6[contains(text(), 'AutoPing Replied')]".format(
                index)  # AutoPing Replied title
            apf = ".//*[@id='outletControl']/div[{0}]/h6[contains(text(), 'AutoPing Failed')]".format(
                index)  # AutoPing Failed title
            wait = WebDriverWait(driver, waitTime)

            outlet_count(outletCount)

            time.sleep(5)
            outletBox.click()

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            # input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            outletClass = driver.get_element_attribute(outletFace, XPATH, ClASS)

            if 'state-on' not in outletClass:
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

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
            wait.until(EC.visibility_of_element_located((By.XPATH, apf)))
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            wait.until(EC.visibility_of_element_located((By.XPATH, apr)))
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # verify that the outlet in the UUT turned back on
            driver.get_element(outletCtrlStr, XPATH)
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.get_element(outletCtrlStr, XPATH)
            driver.element_click(outletCtrlStr, XPATH)
            driver.send_input(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.wait_and_click(outlet_save_btn(), XPATH)

            time.sleep(5)
            outletCount += 1
            index += 1

    @unittest.skip("Skipped for now")
    def test_power_on(self):
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerOn = "//div[8]/div[2]/form[2]/select/option[contains(@value, '3')]"
        outletFace = "//div[8]/div[1]"
        stateBtn = "//div[8]/div[2]/form[1]/button[1]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        frequency = 30
        retries = 2

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)
            outlet_count(outletCount)

            time.sleep(5)
            outletBox.click()

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            # input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            outletClass = driver.get_element_attribute(outletFace, XPATH, ClASS)

            if 'state-off' not in outletClass:
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

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

            time.sleep(frequency * retries)
            time.sleep(10)

            # verify if "AutoPing Failed" is in the autoPing title
            driver.get_element(autoPingTitle, XPATH)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            # verify that the outlet in the UUT turned on
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            self.ctrl_device_power()  # turn outlet back on in the control device

            time.sleep(frequency * retries)

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            driver.get_element(autoPingTitle, XPATH)
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # verify that the outlet in the UUT turned back on
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.get_element(outletCtrlStr, XPATH)
            driver.element_click(outletCtrlStr, XPATH)
            driver.send_input(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.wait_and_click(outlet_save_btn(), XPATH)

            time.sleep(5)
            outletCount += 1
            index += 1

    @unittest.skip("Skipped for now")
    def test_power_on_pending_recovery(self):
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerOnPendRec = "//div[8]/div[2]/form[2]/select/option[contains(@value, '4')]"
        outletFace = "//div[8]/div[1]"
        stateBtn = "//div[8]/div[2]/form[1]/button[1]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        frequency = 30
        retries = 2

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)
            outlet_count(outletCount)

            time.sleep(5)
            outletBox.click()

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            # input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            outletClass = driver.get_element_attribute(outletFace, XPATH, ClASS)

            if 'state-off' not in outletClass:
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

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

            time.sleep(frequency * retries)
            time.sleep(10)
            # verify if "AutoPing Failed" is in the autoPing title
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            time.sleep(frequency * retries)

            # verify that the outlet in the UUT turned back on
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            if 'state-off' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.get_element(outletCtrlStr, XPATH)
            driver.element_click(outletCtrlStr, XPATH)
            driver.send_input(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.wait_and_click(outlet_save_btn(), XPATH)

            time.sleep(5)
            outletCount += 1
            index += 1

    @unittest.skip("Skipped for now")
    def test_power_cycle_once(self):
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerCycleOnce = "//div[8]/div[2]/form[2]/select/option[contains(@value, '5')]"
        outletFace = "//div[8]/div[1]"
        stateBtn = "//div[8]/div[2]/form[1]/button[1]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        cycleDelayElem = "//div[8]/div[2]/form[2]/p[6]/input"
        frequency = 30
        retries = 2
        cycleDelay = 3

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)
            outlet_count(outletCount)

            time.sleep(5)
            outletBox.click()

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            # send input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            outletClass = driver.get_element_attribute(outletFace, XPATH, ClASS)

            if 'state-on' not in outletClass:
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

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

            time.sleep(frequency * retries)
            time.sleep(4)

            driver.get_element(outletCtrlStr, XPATH)
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            print outletClass

            if 'state-off' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # verify if "AutoPing Failed" is in the autoPing title
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            time.sleep(cycleDelay)

            driver.get_element(outletCtrlStr, XPATH)
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            print outletClass

            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            self.ctrl_device_power()  # turn outlet back on in the control device

            # verify that the outlet in the UUT turned back on
            time.sleep(10)
            driver.get_element(outletCtrlStr, XPATH)
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.get_element(outletCtrlStr, XPATH)
            driver.element_click(outletCtrlStr, XPATH)
            driver.send_input(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.wait_and_click(outlet_save_btn(), XPATH)

            time.sleep(5)
            outletCount += 1
            index += 1

    @unittest.skip("Skipped for now")
    def test_power_cycle_until_recovery(self):
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerCycUntilRec = "//div[8]/div[2]/form[2]/select/option[contains(@value, '6')]"
        outletFace = "//div[8]/div[1]"
        stateBtn = "//div[8]/div[2]/form[1]/button[1]"
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        freqInputElem = "//div[8]/div[2]/form[2]/p[2]/input"
        retriesInputElem = "//div[8]/div[2]/form[2]/p[3]/input"
        selectOptions = "//div[8]/div[2]/form[2]/select"
        cycleDelayElem = "//div[8]/div[2]/form[2]/p[6]/input"
        frequency = 30
        retries = 2
        cycleDelay = 3

        outletCount = 1
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            autoPingTitle = "//*[@id='outletControl']/div[{0}]/h6".format(index)
            outlet_count(outletCount)

            time.sleep(5)
            outletBox.click()

            self.ctrl_device_power()  # turn outlet off in the control device

            ipAddresses = get_ip_addresses()
            ipAddressToPing = ipAddresses[2]  # ip address to ping

            # input for ip address to ping, frequency, and retries
            driver.send_input(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.send_input(freqInputElem, XPATH, frequency)
            driver.send_input(retriesInputElem, XPATH, retries)

            outletClass = driver.get_element_attribute(outletFace, XPATH, ClASS)

            if 'state-on' not in outletClass:
                driver.element_click(stateBtn, XPATH)
                driver.element_click("btnOk", ID)
                time.sleep(5)
                driver.get_element(outletCtrlStr, XPATH)
                driver.wait_and_click(outletCtrlStr, XPATH)

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

            time.sleep(frequency * retries)
            time.sleep(4)

            driver.get_element(outletCtrlStr, XPATH)
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            print outletClass

            # verify if "AutoPing Failed" is in the autoPing title
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            time.sleep(cycleDelay)

            driver.get_element(outletCtrlStr, XPATH)
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            print outletClass

            self.ctrl_device_power()  # turn outlet back on in the control device

            time.sleep(10)

            # verify that the outlet in the UUT turned back on
            driver.get_element(outletCtrlStr, XPATH)
            outletClass = driver.get_element_attribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            autoPingTitleClass = driver.get_element_attribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.get_element(outletCtrlStr, XPATH)
            driver.element_click(outletCtrlStr, XPATH)
            driver.send_input(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.wait_and_click(outlet_save_btn(), XPATH)

            time.sleep(5)
            outletCount += 1
            index += 1

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
        driver.element_click(outletCtrlStr, XPATH)
        driver.send_input(ipAddressInputElem, XPATH, "8.8.8.8")
        driver.wait_and_click(outlet_save_btn(), XPATH)
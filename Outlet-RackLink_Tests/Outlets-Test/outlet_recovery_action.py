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
        notify = "//*[@id='notify']"
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
            driver.sendInput(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.sendInput(freqInputElem, XPATH, frequency)
            driver.sendInput(retriesInputElem, XPATH, retries)

            outletClass = driver.getElementAttribute(outletFace, XPATH, ClASS)

            if 'state-on' not in outletClass:
                driver.elementClick(stateBtn, XPATH)
                driver.elementClick("btnOk", ID)
                time.sleep(5)
                driver.getElement(outletCtrlStr, XPATH)
                driver.waitAndClick(outletCtrlStr, XPATH)

            time.sleep(3)
            driver.waitAndClick(selectOptions, XPATH)

            if driver.isElementSelected(powerOffOption, XPATH):
                driver.waitAndClick(outlet_save_btn(), XPATH)
            else:
                driver.waitAndClick(powerOffOption, XPATH)
                self.driver.find_element_by_xpath(powerOffOption).send_keys(Keys.ENTER)
                driver.waitAndClick(outlet_save_btn(), XPATH)

            # in case the notification message to confirm changes pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify).is_displayed()
            if notifyDisplayed:
                driver.elementClick("btnOk", ID)

            # verify if "AutoPing Failed" is in the autoPing title
            wait.until(EC.presence_of_element_located((By.XPATH, apf)))
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            wait.until(EC.presence_of_element_located((By.XPATH, apr)))
            driver.getElement(autoPingTitle, XPATH)
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.getElement(outletCtrlStr, XPATH)
            driver.elementClick(outletCtrlStr, XPATH)
            driver.waitAndClick(stateBtn, XPATH)
            driver.elementClick("btnOk", ID)
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
        notify = "//*[@id='notify']"
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
            driver.sendInput(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.sendInput(freqInputElem, XPATH, frequency)
            driver.sendInput(retriesInputElem, XPATH, retries)

            outletClass = driver.getElementAttribute(outletFace, XPATH, ClASS)

            if 'state-on' not in outletClass:
                driver.elementClick(stateBtn, XPATH)
                driver.elementClick("btnOk", ID)
                time.sleep(5)
                driver.getElement(outletCtrlStr, XPATH)
                driver.waitAndClick(outletCtrlStr, XPATH)

            time.sleep(3)
            driver.waitAndClick(selectOptions, XPATH)

            if driver.isElementSelected(powerOffPendRec, XPATH):
                driver.waitAndClick(outlet_save_btn(), XPATH)
            else:
                driver.waitAndClick(powerOffPendRec, XPATH)
                self.driver.find_element_by_xpath(powerOffPendRec).send_keys(Keys.ENTER)
                driver.waitAndClick(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify).is_displayed()
            if notifyDisplayed:
                driver.elementClick("btnOk", ID)

            # verify if "AutoPing Failed" is in the autoPing title
            wait.until(EC.visibility_of_element_located((By.XPATH, apf)))
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            wait.until(EC.visibility_of_element_located((By.XPATH, apr)))
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # verify that the outlet in the UUT turned back on
            driver.getElement(outletCtrlStr, XPATH)
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.getElement(outletCtrlStr, XPATH)
            driver.elementClick(outletCtrlStr, XPATH)
            driver.sendInput(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.waitAndClick(outlet_save_btn(), XPATH)

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
        notify = "//*[@id='notify']"
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
            driver.sendInput(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.sendInput(freqInputElem, XPATH, frequency)
            driver.sendInput(retriesInputElem, XPATH, retries)

            outletClass = driver.getElementAttribute(outletFace, XPATH, ClASS)

            if 'state-off' not in outletClass:
                driver.elementClick(stateBtn, XPATH)
                driver.elementClick("btnOk", ID)
                time.sleep(5)
                driver.getElement(outletCtrlStr, XPATH)
                driver.waitAndClick(outletCtrlStr, XPATH)

            time.sleep(3)
            driver.waitAndClick(selectOptions, XPATH)

            if driver.isElementSelected(powerOn, XPATH):
                driver.waitAndClick(outlet_save_btn(), XPATH)
            else:
                driver.waitAndClick(powerOn, XPATH)
                self.driver.find_element_by_xpath(powerOn).send_keys(Keys.ENTER)
                driver.waitAndClick(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify).is_displayed()
            if notifyDisplayed:
                driver.elementClick("btnOk", ID)

            time.sleep(frequency * retries)
            time.sleep(10)

            # verify if "AutoPing Failed" is in the autoPing title
            driver.getElement(autoPingTitle, XPATH)
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            # verify that the outlet in the UUT turned on
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            self.ctrl_device_power()  # turn outlet back on in the control device

            time.sleep(frequency * retries)

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            driver.getElement(autoPingTitle, XPATH)
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # verify that the outlet in the UUT turned back on
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.getElement(outletCtrlStr, XPATH)
            driver.elementClick(outletCtrlStr, XPATH)
            driver.sendInput(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.waitAndClick(outlet_save_btn(), XPATH)

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
        notify = "//*[@id='notify']"
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
            driver.sendInput(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.sendInput(freqInputElem, XPATH, frequency)
            driver.sendInput(retriesInputElem, XPATH, retries)

            outletClass = driver.getElementAttribute(outletFace, XPATH, ClASS)

            if 'state-off' not in outletClass:
                driver.elementClick(stateBtn, XPATH)
                driver.elementClick("btnOk", ID)
                time.sleep(5)
                driver.getElement(outletCtrlStr, XPATH)
                driver.waitAndClick(outletCtrlStr, XPATH)

            time.sleep(3)
            driver.waitAndClick(selectOptions, XPATH)

            if driver.isElementSelected(powerOnPendRec, XPATH):
                driver.waitAndClick(outlet_save_btn(), XPATH)
            else:
                driver.waitAndClick(powerOnPendRec, XPATH)
                self.driver.find_element_by_xpath(powerOnPendRec).send_keys(Keys.ENTER)
                driver.waitAndClick(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify).is_displayed()
            if notifyDisplayed:
                driver.elementClick("btnOk", ID)

            time.sleep(frequency * retries)
            time.sleep(10)
            # verify if "AutoPing Failed" is in the autoPing title
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            self.ctrl_device_power()  # turn outlet back on in the control device

            time.sleep(frequency * retries)

            # verify that the outlet in the UUT turned back on
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            if 'state-off' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.getElement(outletCtrlStr, XPATH)
            driver.elementClick(outletCtrlStr, XPATH)
            driver.sendInput(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.waitAndClick(outlet_save_btn(), XPATH)

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
        notify = "//*[@id='notify']"
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
            driver.sendInput(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.sendInput(freqInputElem, XPATH, frequency)
            driver.sendInput(retriesInputElem, XPATH, retries)

            outletClass = driver.getElementAttribute(outletFace, XPATH, ClASS)

            if 'state-on' not in outletClass:
                driver.elementClick(stateBtn, XPATH)
                driver.elementClick("btnOk", ID)
                time.sleep(5)
                driver.getElement(outletCtrlStr, XPATH)
                driver.waitAndClick(outletCtrlStr, XPATH)

            time.sleep(3)
            driver.waitAndClick(selectOptions, XPATH)

            if driver.isElementSelected(powerCycleOnce, XPATH):
                driver.waitAndClick(outlet_save_btn(), XPATH)
            else:
                driver.waitAndClick(powerCycleOnce, XPATH)
                self.driver.find_element_by_xpath(powerCycleOnce).send_keys(Keys.ENTER)
                driver.waitForElement(cycleDelayElem, XPATH)
                driver.sendInput(cycleDelayElem, XPATH, cycleDelay)
                driver.waitAndClick(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify).is_displayed()
            if notifyDisplayed:
                driver.elementClick("btnOk", ID)

            time.sleep(frequency * retries)
            time.sleep(4)

            driver.getElement(outletCtrlStr, XPATH)
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            print outletClass

            if 'state-off' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # verify if "AutoPing Failed" is in the autoPing title
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            time.sleep(cycleDelay)

            driver.getElement(outletCtrlStr, XPATH)
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            print outletClass

            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            self.ctrl_device_power()  # turn outlet back on in the control device

            # verify that the outlet in the UUT turned back on
            time.sleep(10)
            driver.getElement(outletCtrlStr, XPATH)
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.getElement(outletCtrlStr, XPATH)
            driver.elementClick(outletCtrlStr, XPATH)
            driver.sendInput(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.waitAndClick(outlet_save_btn(), XPATH)

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
        notify = "//*[@id='notify']"
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
            driver.sendInput(ipAddressInputElem, XPATH, ipAddressToPing)
            driver.sendInput(freqInputElem, XPATH, frequency)
            driver.sendInput(retriesInputElem, XPATH, retries)

            outletClass = driver.getElementAttribute(outletFace, XPATH, ClASS)

            if 'state-on' not in outletClass:
                driver.elementClick(stateBtn, XPATH)
                driver.elementClick("btnOk", ID)
                time.sleep(5)
                driver.getElement(outletCtrlStr, XPATH)
                driver.waitAndClick(outletCtrlStr, XPATH)

            time.sleep(3)
            driver.waitAndClick(selectOptions, XPATH)

            if driver.isElementSelected(powerCycUntilRec, XPATH):
                driver.waitAndClick(outlet_save_btn(), XPATH)
            else:
                driver.waitAndClick(powerCycUntilRec, XPATH)
                self.driver.find_element_by_xpath(powerCycUntilRec).send_keys(Keys.ENTER)
                driver.waitForElement(cycleDelayElem, XPATH)
                driver.sendInput(cycleDelayElem, XPATH, cycleDelay)
                driver.waitAndClick(outlet_save_btn(), XPATH)

            # in case the notification message pops up
            notifyDisplayed = self.driver.find_element_by_xpath(notify).is_displayed()
            if notifyDisplayed:
                driver.elementClick("btnOk", ID)

            time.sleep(frequency * retries)
            time.sleep(4)

            driver.getElement(outletCtrlStr, XPATH)
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            print outletClass

            # verify if "AutoPing Failed" is in the autoPing title
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Failed"

            time.sleep(cycleDelay)

            driver.getElement(outletCtrlStr, XPATH)
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            print outletClass

            self.ctrl_device_power()  # turn outlet back on in the control device

            time.sleep(10)

            # verify that the outlet in the UUT turned back on
            driver.getElement(outletCtrlStr, XPATH)
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            if 'state-on' in outletClass:
                state = True
            else:
                state = False
            assert state == True

            # gets class again and verify if "AutoPing Replied" is in the autoPing title
            autoPingTitleClass = driver.getElementAttribute(autoPingTitle, XPATH, "title")
            print autoPingTitleClass
            assert autoPingTitleClass == "AutoPing Replied"

            # open outlet in UUT, turn it back on, change ip address to default, & save changes
            time.sleep(3)
            driver.getElement(outletCtrlStr, XPATH)
            driver.elementClick(outletCtrlStr, XPATH)
            driver.sendInput(ipAddressInputElem, XPATH, "8.8.8.8")
            driver.waitAndClick(outlet_save_btn(), XPATH)

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
        ctrlDriver.elementClick(outlet3, XPATH)

        # turn outlet off and close success message alert
        time.sleep(3)
        ctrlDriver.waitAndClick(stateBtn, XPATH)
        ctrlDriver.waitAndClick("btnOk", ID)
        ctrlDriver.waitAndClick(close_btn_msg(), XPATH)

        time.sleep(3)
        self.ctrlDriver.quit()

    def change_ip_address_to_default(self, outletCtrlStr, ipAddressInputElem):
        driver = SeleniumDriver(self.driver)
        driver.getElement(outletCtrlStr, XPATH)
        driver.elementClick(outletCtrlStr, XPATH)
        driver.sendInput(ipAddressInputElem, XPATH, "8.8.8.8")
        driver.waitAndClick(outlet_save_btn(), XPATH)
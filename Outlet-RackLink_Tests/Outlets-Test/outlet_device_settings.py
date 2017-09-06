# coding=utf-8

import time
from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from selenium.webdriver.support.ui import Select
from Utils.string_constants import *


class OutletDeviceSettings(TestFixtures):
    def restore_device_settings(self):
        driver = SeleniumDriver(self.driver)
        menuIcon = ".//*[@id='wrapper']/header/i"
        factoryDefaults = "//nav/ul/li[5]"
        restoreDeviceSet = "//*[@id='factoryDefaults']/p[6]/input"
        saveBtn = ".//*[@id='spbg']/button[2]"

        driver.waitAndClick(menuIcon, XPATH)
        time.sleep(3)
        driver.forceClick(factoryDefaults, XPATH)

        time.sleep(3)

        driver.elementClick(restoreDeviceSet, XPATH)
        driver.waitAndClick(saveBtn, XPATH)

        time.sleep(11)  # wait for 10 seconds plus another second to click on OK button
        driver.elementClick("btnOk", ID)

    def open_device_settings(self):
        menuIcon = ".//*[@id='wrapper']/header/i"
        deviceSettings = "//nav/ul/li[3]"

        driver = SeleniumDriver(self.driver)
        driver.getElement(menuIcon, XPATH)
        driver.waitAndClick(menuIcon, XPATH)
        time.sleep(3)
        driver.forceClick(deviceSettings, XPATH)

    # -------------------- Tests --------------------------------

    # @unittest.skip("Skipped for now")
    def test_device_name(self):
        driver = SeleniumDriver(self.driver)
        deviceName = "//*[@id='deviceSettings']/p[2]/input"
        saveBtn = "//*[@id='spbg']/button[2]"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        deviceNameDefault = driver.getElementAttribute(deviceName, XPATH, VALUE)

        time.sleep(3)
        driver.sendInput(deviceName, XPATH, "Unit Under Test.")

        driver.waitAndClick(saveBtn, XPATH)
        driver.waitAndClick(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.getElement(deviceName, XPATH)
        changedDeviceName = driver.getElementAttribute(deviceName, XPATH, VALUE)

        assert deviceNameDefault != changedDeviceName

    def test_account_name_number(self):
        driver = SeleniumDriver(self.driver)
        accountNameNum = "//*[@id='deviceSettings']/p[3]/input"
        saveBtn = "//*[@id='spbg']/button[2]"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        acctNameNumDefault = driver.getElementAttribute(accountNameNum, XPATH, VALUE)

        time.sleep(3)
        driver.sendInput(accountNameNum, XPATH, "1234567890")

        driver.waitAndClick(saveBtn, XPATH)
        driver.waitAndClick(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.getElement(accountNameNum, XPATH)
        changedAcctNameNum = driver.getElementAttribute(accountNameNum, XPATH, VALUE)

        assert acctNameNumDefault != changedAcctNameNum

    def test_device_description(self):
        driver = SeleniumDriver(self.driver)
        descriptionInput = "//*[@id='deviceSettings']/p[4]/input"
        saveBtn = "//*[@id='spbg']/button[2]"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        descriptionDefault = driver.getElementAttribute(descriptionInput, XPATH, VALUE)

        time.sleep(3)
        driver.sendInput(descriptionInput, XPATH, "This is the description.")

        driver.waitAndClick(saveBtn, XPATH)
        driver.waitAndClick(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.getElement(descriptionInput, XPATH)
        changedDescription = driver.getElementAttribute(descriptionInput, XPATH, VALUE)

        assert descriptionDefault != changedDescription

    def test_device_location(self):
        driver = SeleniumDriver(self.driver)
        locationInput = "//*[@id='deviceSettings']/p[5]/input"
        saveBtn = "//*[@id='spbg']/button[2]"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        locationDefault = driver.getElementAttribute(locationInput, XPATH, VALUE)

        time.sleep(3)
        driver.sendInput(locationInput, XPATH, "The UUT is at this location.")

        driver.waitAndClick(saveBtn, XPATH)
        driver.waitAndClick(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.getElement(locationInput, XPATH)
        changedLocation = driver.getElementAttribute(locationInput, XPATH, VALUE)

        assert locationDefault != changedLocation

    def test_initial_outlet_state(self):
        driver = SeleniumDriver(self.driver)
        iniOutletStateSelect = "//*[@id='deviceSettings']/p[6]/select"
        rememberPriorState = "//*[@id='deviceSettings']/p[6]/select/option[1]"
        saveBtn = "//*[@id='spbg']/button[2]"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        time.sleep(3)
        driver.waitAndClick(iniOutletStateSelect, XPATH)

        time.sleep(3)
        driver.waitAndClick(rememberPriorState, XPATH)

        driver.waitAndClick(saveBtn, XPATH)
        driver.waitAndClick(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        select = Select(self.driver.find_element_by_xpath(iniOutletStateSelect))
        selected_option = select.first_selected_option

        if selected_option.text == 'Remember prior state':
            correctSelect = True
        else:
            correctSelect = False

        assert correctSelect == True

    def test_seq_power_up(self):
        driver = SeleniumDriver(self.driver)
        sequenceState = "sequenceState"
        saveBtn = "//*[@id='spbg']/button[2]"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        sequenceStateDefault = driver.getElementAttribute(sequenceState, ID, ClASS)
        print sequenceStateDefault

        time.sleep(3)
        driver.waitAndClick(sequenceState, ID)

        driver.waitAndClick(saveBtn, XPATH)
        driver.waitAndClick(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.getElement(sequenceState, ID)
        changedSequenceState = driver.getElementAttribute(sequenceState, ID, ClASS)
        print changedSequenceState

        assert sequenceStateDefault != changedSequenceState

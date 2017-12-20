# coding=utf-8

import time
from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from selenium.webdriver.support.ui import Select
from Utils.string_constants import *


class DeviceSettings(TestFixtures):

    # @unittest.skip("Skipped for now")
    def test_device_name(self):
        driver = SeleniumDriver(self.driver)
        deviceName = "//*[@id='deviceSettings']/p[2]/input"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        deviceNameDefault = driver.get_element_attribute(deviceName, XPATH, VALUE)

        time.sleep(3)
        driver.send_input(deviceName, XPATH, "Unit Under Test.")

        driver.wait_and_click(save_btn(), XPATH)
        driver.wait_and_click(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.get_element(deviceName, XPATH)
        changedDeviceName = driver.get_element_attribute(deviceName, XPATH, VALUE)

        assert deviceNameDefault != changedDeviceName

    def test_account_name_number(self):
        driver = SeleniumDriver(self.driver)
        accountNameNum = "//*[@id='deviceSettings']/p[3]/input"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        acctNameNumDefault = driver.get_element_attribute(accountNameNum, XPATH, VALUE)

        time.sleep(3)
        driver.send_input(accountNameNum, XPATH, "1234567890")

        driver.wait_and_click(save_btn(), XPATH)
        driver.wait_and_click(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.get_element(accountNameNum, XPATH)
        changedAcctNameNum = driver.get_element_attribute(accountNameNum, XPATH, VALUE)

        assert acctNameNumDefault != changedAcctNameNum

    def test_device_description(self):
        driver = SeleniumDriver(self.driver)
        descriptionInput = "//*[@id='deviceSettings']/p[4]/input"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        descriptionDefault = driver.get_element_attribute(descriptionInput, XPATH, VALUE)

        time.sleep(3)
        driver.send_input(descriptionInput, XPATH, "This is the description.")

        driver.wait_and_click(save_btn(), XPATH)
        driver.wait_and_click(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.get_element(descriptionInput, XPATH)
        changedDescription = driver.get_element_attribute(descriptionInput, XPATH, VALUE)

        assert descriptionDefault != changedDescription

    def test_device_location(self):
        driver = SeleniumDriver(self.driver)
        locationInput = "//*[@id='deviceSettings']/p[5]/input"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        locationDefault = driver.get_element_attribute(locationInput, XPATH, VALUE)

        time.sleep(3)
        driver.send_input(locationInput, XPATH, "The UUT is at this location.")

        driver.wait_and_click(save_btn(), XPATH)
        driver.wait_and_click(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.get_element(locationInput, XPATH)
        changedLocation = driver.get_element_attribute(locationInput, XPATH, VALUE)

        assert locationDefault != changedLocation

    def test_initial_outlet_state(self):
        driver = SeleniumDriver(self.driver)
        iniOutletStateSelect = "//*[@id='deviceSettings']/p[6]/select"
        rememberPriorState = "//*[@id='deviceSettings']/p[6]/select/option[1]"

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        time.sleep(3)
        driver.wait_and_click(iniOutletStateSelect, XPATH)

        time.sleep(3)
        driver.wait_and_click(rememberPriorState, XPATH)

        driver.wait_and_click(save_btn(), XPATH)
        driver.wait_and_click(close_btn_msg(), XPATH)

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

        self.restore_device_settings()
        time.sleep(3)
        self.open_device_settings()

        sequenceStateDefault = driver.get_element_attribute(sequenceState, ID, ClASS)

        time.sleep(3)
        driver.wait_and_click(sequenceState, ID)

        driver.wait_and_click(save_btn(), XPATH)
        driver.wait_and_click(close_btn_msg(), XPATH)

        time.sleep(3)
        self.open_device_settings()

        driver.get_element(sequenceState, ID)
        changedSequenceState = driver.get_element_attribute(sequenceState, ID, ClASS)

        assert sequenceStateDefault != changedSequenceState

    # -------------------- Functions --------------------------------

    def open_device_settings(self):
        menuIcon = ".//*[@id='wrapper']/header/i"
        deviceSettings = "//nav/ul/li[3]"

        driver = SeleniumDriver(self.driver)
        driver.get_element(menuIcon, XPATH)
        driver.wait_and_click(menuIcon, XPATH)
        time.sleep(3)
        driver.force_click(deviceSettings, XPATH)

    def restore_device_settings(self):
        driver = SeleniumDriver(self.driver)
        factoryDefaults = "//nav/ul/li[5]"
        restoreDeviceSet = "//*[@id='factoryDefaults']/p[6]/input"

        driver.wait_and_click(menu(), XPATH)
        time.sleep(3)
        driver.force_click(factoryDefaults, XPATH)

        time.sleep(3)

        driver.element_click(restoreDeviceSet, XPATH)
        driver.wait_and_click(save_btn(), XPATH)

        time.sleep(11)  # wait for 10 seconds plus another second to click on OK button
        driver.element_click("btnOk", ID)

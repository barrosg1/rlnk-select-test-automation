# coding=utf-8

import time
import unittest
from Utils.fixtures_test import TestFixtures
from selenium.webdriver.common.action_chains import ActionChains
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletDateTime(TestFixtures):
    def restore_date_time(self):
        driver = SeleniumDriver(self.driver)
        menuIcon = ".//*[@id='wrapper']/header/i"
        factoryDefaults = "//nav/ul/li[5]"
        restoreDateTime = "//*[@id='factoryDefaults']/p[5]/input"
        saveBtn = ".//*[@id='spbg']/button[2]"

        driver.waitAndClick(menuIcon, XPATH)
        time.sleep(3)
        driver.forceClick(factoryDefaults, XPATH)

        time.sleep(3)

        driver.elementClick(restoreDateTime, XPATH)
        driver.waitAndClick(saveBtn, XPATH)

        time.sleep(11)  # wait for 10 seconds plus another second to click on OK button
        driver.elementClick("btnOk", ID)

    @unittest.skip("Skipped for now")
    def test_date_time(self):
        driver = SeleniumDriver(self.driver)
        menuIcon = ".//*[@id='wrapper']/header/i"
        dateTime = "//nav/ul/li[2]"
        timeZone = "//*[@id='dt_tz']/option[1]"
        enableDaySav = "//*[@id='dateTimeSettings']/div[2]/input"
        saveBtn = "//*[@id='spbg']/button[2]"

        self.restore_date_time()
        time.sleep(3)
        driver.waitAndClick(menuIcon, XPATH)
        driver.waitAndClick(dateTime, XPATH)

        time.sleep(3)
        if driver.isElementSelected(enableDaySav, XPATH):
            driver.elementClick(enableDaySav, XPATH)

        time.sleep(3)
        driver.waitAndClick("dt_tz", ID)
        driver.waitAndClick(timeZone, XPATH)

        driver.elementClick(saveBtn, XPATH)
        driver.waitAndClick(close_btn_msg(), XPATH)

        time.sleep(3)
        driver.getElement(menuIcon, XPATH)
        driver.waitAndClick(menuIcon, XPATH)
        driver.waitAndClick(dateTime, XPATH)

    @unittest.skip("Skipped for now")
    def test_NTP(self):
        driver = SeleniumDriver(self.driver)
        menuIcon = ".//*[@id='wrapper']/header/i"
        dateTime = "//nav/ul/li[2]"
        ntpEnabled = "//*[@id='dateTimeSettings']/div[3]/button"
        yearInput = "//*[@id='dateTimeSettings']/div[3]/p[3]/input[1]"
        monthInput = "//*[@id='dateTimeSettings']/div[3]/p[3]/input[2]"
        dayInput = "//*[@id='dateTimeSettings']/div[3]/p[3]/input[3]"
        hourInput = "//*[@id='dateTimeSettings']/div[3]/p[4]/input[1]"
        minuteInput = "//*[@id='dateTimeSettings']/div[3]/p[4]/input[2]"
        btnAPM = "//*[@id='dateTimeSettings']/div[3]/p[4]/button"  # AM | PM button
        saveBtn = "//*[@id='spbg']/button[2]"

        # restore date/time back to default
        self.restore_date_time()
        time.sleep(3)

        # open menu and select date/time settings
        driver.getElement(menuIcon, XPATH)
        driver.waitAndClick(menuIcon, XPATH)
        driver.waitAndClick(dateTime, XPATH)

        # if ntp button is enabled, click to switch to MAN (manual)
        ntpEnabledClass = driver.getElementAttribute(ntpEnabled, XPATH, ClASS)
        if 'state1' in ntpEnabledClass:
            time.sleep(3)
            driver.forceClick(ntpEnabled, XPATH)

        # invalid year, month, and day
        driver.sendInput(yearInput, XPATH, "yyyy")
        driver.sendInput(monthInput, XPATH, "mm")
        driver.sendInput(dayInput, XPATH, "dd")

        driver.waitAndClick(saveBtn, XPATH)
        driver.waitAndClick("btnOk", ID)

        # acceptable year, month, and day
        driver.sendInput(yearInput, XPATH, "2000")
        driver.sendInput(monthInput, XPATH, "02")
        driver.sendInput(dayInput, XPATH, "20")

        # invalid hour and minute input
        driver.sendInput(hourInput, XPATH, "22")
        driver.sendInput(minuteInput, XPATH, "68")

        driver.waitAndClick(saveBtn, XPATH)
        driver.waitAndClick("btnOk", ID)

        # acceptable hour and minute input
        driver.sendInput(hourInput, XPATH, "8")
        driver.sendInput(minuteInput, XPATH, "20")

        # if button already in AM mode, click to switch to PM mode
        btnAPMClass = driver.getElementAttribute(btnAPM, XPATH, ClASS)
        if 'state1' in btnAPMClass:
            driver.waitAndClick(btnAPM, XPATH)

        driver.waitAndClick(saveBtn, XPATH)
        driver.waitAndClick(close_btn_msg(), XPATH)
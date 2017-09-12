# coding=utf-8

import time
import unittest
from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *


class DateTimeSettings(TestFixtures):

    #@unittest.skip("Skipped for now")
    def test_date_time(self):
        driver = SeleniumDriver(self.driver)
        dateTime = "//nav/ul/li[2]"
        timeZone = "//*[@id='dt_tz']/option[1]"
        enableDaySav = "//*[@id='dateTimeSettings']/div[2]/input"

        self.restore_date_time()
        time.sleep(3)
        driver.wait_and_click(menu(), XPATH)
        driver.wait_and_click(dateTime, XPATH)

        time.sleep(3)
        if driver.is_element_selected(enableDaySav, XPATH):
            driver.element_click(enableDaySav, XPATH)

        time.sleep(3)
        driver.wait_and_click("dt_tz", ID)
        driver.wait_and_click(timeZone, XPATH)

        driver.element_click(save_btn(), XPATH)
        driver.wait_and_click(close_btn_msg(), XPATH)

        time.sleep(3)
        driver.get_element(menu(), XPATH)
        driver.wait_and_click(menu(), XPATH)
        driver.wait_and_click(dateTime, XPATH)

    #@unittest.skip("Skipped for now")
    def test_NTP(self):
        driver = SeleniumDriver(self.driver)
        dateTime = "//nav/ul/li[2]"
        ntpEnabled = "//*[@id='dateTimeSettings']/div[3]/button"
        yearInput = "//*[@id='dateTimeSettings']/div[3]/p[3]/input[1]"
        monthInput = "//*[@id='dateTimeSettings']/div[3]/p[3]/input[2]"
        dayInput = "//*[@id='dateTimeSettings']/div[3]/p[3]/input[3]"
        hourInput = "//*[@id='dateTimeSettings']/div[3]/p[4]/input[1]"
        minuteInput = "//*[@id='dateTimeSettings']/div[3]/p[4]/input[2]"
        btnAPM = "//*[@id='dateTimeSettings']/div[3]/p[4]/button"  # AM | PM button

        # restore date/time back to default
        self.restore_date_time()
        time.sleep(3)

        # open menu and select date/time settings
        driver.get_element(menu(), XPATH)
        driver.wait_and_click(menu(), XPATH)
        driver.wait_and_click(dateTime, XPATH)

        # if ntp button is enabled, click to switch to MAN (manual)
        ntpEnabledClass = driver.get_element_attribute(ntpEnabled, XPATH, ClASS)
        if 'state1' in ntpEnabledClass:
            time.sleep(3)
            driver.force_click(ntpEnabled, XPATH)

        # invalid year, month, and day
        driver.send_input(yearInput, XPATH, "yyyy")
        driver.send_input(monthInput, XPATH, "mm")
        driver.send_input(dayInput, XPATH, "dd")

        driver.wait_and_click(save_btn(), XPATH)
        driver.wait_and_click("btnOk", ID)

        # acceptable year, month, and day
        driver.send_input(yearInput, XPATH, "2000")
        driver.send_input(monthInput, XPATH, "02")
        driver.send_input(dayInput, XPATH, "20")

        # invalid hour and minute input
        driver.send_input(hourInput, XPATH, "22")
        driver.send_input(minuteInput, XPATH, "68")

        driver.wait_and_click(save_btn(), XPATH)
        driver.wait_and_click("btnOk", ID)

        # acceptable hour and minute input
        driver.send_input(hourInput, XPATH, "8")
        driver.send_input(minuteInput, XPATH, "20")

        # if button already in AM mode, click to switch to PM mode
        btnAPMClass = driver.get_element_attribute(btnAPM, XPATH, ClASS)
        if 'state1' in btnAPMClass:
            driver.wait_and_click(btnAPM, XPATH)

        driver.wait_and_click(save_btn(), XPATH)
        driver.wait_and_click(close_btn_msg(), XPATH)

    # -------------------- Functions --------------------------------

    def restore_date_time(self):
        driver = SeleniumDriver(self.driver)
        factoryDefaults = "//nav/ul/li[5]"
        restoreDateTime = "//*[@id='factoryDefaults']/p[5]/input"

        driver.wait_and_click(menu(), XPATH)
        time.sleep(3)
        driver.force_click(factoryDefaults, XPATH)

        time.sleep(3)

        driver.element_click(restoreDateTime, XPATH)
        driver.wait_and_click(save_btn(), XPATH)

        time.sleep(11)  # wait for 10 seconds plus another second to click on OK button
        driver.element_click("btnOk", ID)
# coding=utf-8

import time
import unittest
from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletEmailSettings(TestFixtures):

    # -------------------- Tests --------------------------------

    @unittest.skip("Skipped for now")
    def test_ip_host_name(self):
        driver = SeleniumDriver(self.driver)
        emailIpHost = "//*[@id='emailSettings']/div[1]/p[1]/input"
        saveBtn = "//*[@id='spbg']/button[2]"
        cancelBtn = "//*[@id='spbg']/button[1]"
        notifyMsg = "//*[@id='notify']"
        inputBox = "//*[@id='emailSettings']/div[1]/p[1]/input"
        invalidIpHostNames = ['0.8.8.8', '8.8.8.0', '255.8.8.8', '20.255.90',
                              '8.8.8', '8.8.8.8.8', 'exchange.map']

        self.open_email_settings()
        time.sleep(3)
        self.default_ip_email_rep()
        time.sleep(3)

        for name in invalidIpHostNames:
            driver.waitUntilClickable(emailIpHost, XPATH)
            driver.sendInput(emailIpHost, XPATH, name)
            driver.waitAndClick(saveBtn, XPATH)

            ipHostVal = driver.getElementAttribute(emailIpHost, XPATH, VALUE)
            ipNodes = ip_nodes(ipHostVal)
            hostNodes = host_nodes(ipHostVal)

            assert self.has_error(inputBox) == True
            assert self.is_hidden_string(notifyMsg) == False

            driver.elementClick("btnOk", ID)
            ipInputClass = driver.getElementAttribute(emailIpHost, XPATH, ClASS)

            expectedOpGood = True

            if name.startswith("0"):
                assert starts_with_zero(ipHostVal, ipInputClass) == expectedOpGood
            elif name.endswith("0"):
                assert ends_with_zero(ipHostVal, ipInputClass) == expectedOpGood
            elif "255" in name:
                assert node_255(ipHostVal, ipInputClass) == expectedOpGood
            elif len(ipNodes) < 4:
                assert short_ip_node_length(ipHostVal, ipInputClass) == expectedOpGood
            elif len(hostNodes) < 3:
                assert short_host_node_length(ipHostVal, ipInputClass) == expectedOpGood
            else:
                assert long_ip_node_length(ipHostVal, ipInputClass) == expectedOpGood

        driver.waitAndClick(cancelBtn, XPATH)

        time.sleep(3)
        self.restore_device_settings()

    @unittest.skip("Skipped for now")
    def test_sender_email(self):
        driver = SeleniumDriver(self.driver)
        send_email_input = "//*[@id='emailSettings']/div[1]/p[2]/input"
        saveBtn = "//*[@id='spbg']/button[2]"
        cancelBtn = "//*[@id='spbg']/button[1]"
        notifyMsg = "//*[@id='notify']"
        invalid_emails = ['test@@test.com', 'test@test..com',
                          '@.com', 'test', 'test.com', 'test@t.c', '']

        self.open_email_settings()
        time.sleep(3)
        self.default_ip_email_rep()
        time.sleep(3)

        for email in invalid_emails:
            driver.waitUntilClickable(send_email_input, XPATH)
            driver.sendInput(send_email_input, XPATH, email)
            driver.waitAndClick(saveBtn, XPATH)

            assert self.has_error(send_email_input) == True
            assert self.is_hidden_string(notifyMsg) == False

            driver.elementClick("btnOk", ID)
        driver.waitAndClick(cancelBtn, XPATH)

        time.sleep(3)
        self.restore_device_settings()

    @unittest.skip("Skipped for now")
    def test_port_number(self):
        driver = SeleniumDriver(self.driver)
        port_input = "//*[@id='emailSettings']/div[1]/p[3]/input"
        saveBtn = "//*[@id='spbg']/button[2]"
        cancelBtn = "//*[@id='spbg']/button[1]"
        notifyMsg = "//*[@id='notify']"
        invalid_ports = ['test', 'test123', '---']

        self.open_email_settings()
        time.sleep(3)
        self.default_ip_email_rep()
        time.sleep(3)

        for port in invalid_ports:
            driver.waitUntilClickable(port_input, XPATH)
            driver.sendInput(port_input, XPATH, port)
            driver.waitAndClick(saveBtn, XPATH)

            assert self.has_error(port_input) == True
            assert self.is_hidden_string(notifyMsg) == False

            driver.elementClick("btnOk", ID)
        driver.waitAndClick(cancelBtn, XPATH)

        time.sleep(3)
        self.restore_device_settings()

    @unittest.skip("Skipped for now")
    def test_authentication(self):
        driver = SeleniumDriver(self.driver)
        username = "//*[@id='emailSettings']/div[2]/p[2]/input"
        password = "//*[@id='emailSettings']/div[2]/p[3]/input[1]"
        confirmPass = "//*[@id='emailSettings']/div[2]/p[4]/input[1]"
        showPass = "//*[@id='emailSettings']/div[2]/p[5]/input"  # show password
        saveBtn = "//*[@id='spbg']/button[2]"
        cancelBtn = "//*[@id='spbg']/button[1]"
        notifyMsg = "//*[@id='notify']"

        self.open_email_settings()
        self.default_ip_email_rep()
        time.sleep(3)

        driver.waitAndClick("authReq", ID)
        driver.waitAndClick(saveBtn, XPATH)

        assert self.has_error(username) == True
        assert self.has_error(password) == True
        assert self.has_error(confirmPass) == True
        assert self.is_hidden_string(notifyMsg) == False

        driver.elementClick("btnOk", ID)

        time.sleep(3)
        driver.waitForVisibility(password, XPATH)
        driver.getElement(password, XPATH)
        driver.sendInput(password, XPATH, "Test123")

        driver.getElement(confirmPass, XPATH)
        driver.sendInput(confirmPass, XPATH, "Test123")

        driver.elementClick(showPass, XPATH)
        if driver.isElementSelected(showPass, XPATH):
            # if 'hidden' is in the password class
            assert self.is_hidden_string(password) == True

            time.sleep(3)
            driver.elementClick(showPass, XPATH)

            # if 'hidden' is not in the password class
            assert self.is_hidden_string(password) == False

        driver.waitAndClick(cancelBtn, XPATH)

        time.sleep(3)
        self.restore_device_settings()

    # @unittest.skip("Skipped for now")
    def test_recipients(self):
        driver = SeleniumDriver(self.driver)
        addRepBtn = "//*[@id='emailSettings']/div[3]/p[2]/button"  # add recipient button
        removeRepBox = "//*[@id='emailSettings']/div[3]/div[" \
                       "not(contains(@class, 'recpEntry hidden'))]/p[1]/b/span"
        send_email_btn = "//*[@id='emailSettings']/p/button"
        emailIpHost = "//*[@id='emailSettings']/div[1]/p[1]/input"
        send_email_input = "//*[@id='emailSettings']/div[1]/p[2]/input"
        successMsg = "//*[@id='successMsg']"
        cancelBtn = "//*[@id='spbg']/button[1]"

        self.open_email_settings()
        time.sleep(3)

        driver.sendInput(emailIpHost, XPATH, "8.8.8.8")
        driver.sendInput(send_email_input, XPATH, "test123t@middleatlantic.com")

        time.sleep(3)

        rep_div_count = 0  # number of "recpEntry" div
        i = 2
        for x in range(0, 5):
            repName = "//*[@id='emailSettings']/div[3]/div[{0}]/p[1]/input".format(i)
            repEmail = "//*[@id='emailSettings']/div[3]/div[{0}]/p[2]/input".format(i)
            time.sleep(2)
            driver.getElement(addRepBtn, XPATH)
            driver.waitAndClick(addRepBtn, XPATH)

            time.sleep(2)
            driver.sendInput(repName, XPATH, "Test Test")
            driver.sendInput(repEmail, XPATH, "test.test@middleatlantic.com")
            rep_div_count += 1

            i += 1

        assert rep_div_count == 5

        driver.waitAndClick(send_email_btn, XPATH)
        time.sleep(3)

        assert self.is_hidden_string(successMsg) == False
        driver.waitAndClick(close_btn_msg(), XPATH)

        # get removeRepBoxList, length should be 5
        removeRepBoxList = self.driver.find_elements_by_xpath(removeRepBox)
        i = 2
        for x in removeRepBoxList:
            removeRepBox = "//*[@id='emailSettings']/div[3]/div[{0}]/p[1]/b/span".format(i)
            time.sleep(3)
            driver.waitAndClick(removeRepBox, XPATH)

        # get removeRepBoxList again, length should be 0
        removeRepBoxList = self.driver.find_elements_by_xpath(removeRepBox)

        assert len(removeRepBoxList) == 0

        driver.waitAndClick(cancelBtn, XPATH)

        time.sleep(3)
        self.restore_device_settings()

    # -------------------- Functions --------------------------------

    def restore_device_settings(self):
        driver = SeleniumDriver(self.driver)
        menuIcon = ".//*[@id='wrapper']/header/i"
        factoryDefaults = "//nav/ul/li[5]"
        restoreEmailSett = "//*[@id='factoryDefaults']/p[7]/input"
        saveBtn = ".//*[@id='spbg']/button[2]"

        driver.waitAndClick(menuIcon, XPATH)
        time.sleep(3)
        driver.forceClick(factoryDefaults, XPATH)

        time.sleep(3)
        driver.elementClick(restoreEmailSett, XPATH)
        driver.waitAndClick(saveBtn, XPATH)

        time.sleep(11)  # wait for 10 seconds plus another second to click on OK button
        driver.elementClick("btnOk", ID)

    def open_email_settings(self):
        menuIcon = ".//*[@id='wrapper']/header/i"
        emailSettings = "//nav/ul/li[4]"

        driver = SeleniumDriver(self.driver)
        driver.getElement(menuIcon, XPATH)
        driver.waitAndClick(menuIcon, XPATH)

        time.sleep(3)
        driver.forceClick(emailSettings, XPATH)

    def default_ip_email_rep(self):
        driver = SeleniumDriver(self.driver)
        emailIpHost = "//*[@id='emailSettings']/div[1]/p[1]/input"
        senderEmail = "//*[@id='emailSettings']/div[1]/p[2]/input"
        addRepBtn = "//*[@id='emailSettings']/div[3]/p[2]/button"  # add recipient button
        repName = "//*[@id='emailSettings']/div[3]/div[2]/p[1]/input"
        repEmail = "//*[@id='emailSettings']/div[3]/div[2]/p[2]/input"
        recpEntry = "//*[@id='emailSettings']/div[3]/div[2]"

        if not driver.isElementPresent(recpEntry, XPATH):
            driver.waitAndClick(addRepBtn, XPATH)
            time.sleep(3)

        driver.sendInput(emailIpHost, XPATH, "12.12.12.12")
        driver.sendInput(senderEmail, XPATH, "test@test.com")

        driver.sendInput(repName, XPATH, "Test Test")
        driver.sendInput(repEmail, XPATH, "test.test@middleatlantic.com")



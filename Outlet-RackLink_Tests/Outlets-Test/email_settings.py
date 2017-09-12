# coding=utf-8

import time
import unittest
from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class EmailSettings(TestFixtures):

    # -------------------- Tests --------------------------------

    @unittest.skip("Skipped for now")
    def test_ip_host_name(self):
        driver = SeleniumDriver(self.driver)
        emailIpHost = "//*[@id='emailSettings']/div[1]/p[1]/input"
        inputBox = "//*[@id='emailSettings']/div[1]/p[1]/input"
        invalidIpHostNames = ['0.8.8.8', '8.8.8.0', '255.8.8.8', '20.255.90',
                              '8.8.8', '8.8.8.8.8', 'exchange.map']

        self.open_email_settings()
        time.sleep(3)
        self.default_ip_email_rep()
        time.sleep(3)

        for name in invalidIpHostNames:
            driver.wait_until_clickable(emailIpHost, XPATH)
            driver.send_input(emailIpHost, XPATH, name)
            driver.wait_and_click(save_btn(), XPATH)

            ipHostVal = driver.get_element_attribute(emailIpHost, XPATH, VALUE)
            ipNodes = ip_nodes(ipHostVal)
            hostNodes = host_nodes(ipHostVal)

            assert self.has_error(inputBox) == True
            assert self.is_hidden_string(notify_msg()) == False

            driver.element_click("btnOk", ID)
            ipInputClass = driver.get_element_attribute(emailIpHost, XPATH, ClASS)

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

        driver.wait_and_click(cancel_btn(), XPATH)

        time.sleep(3)
        self.restore_email_settings()

    @unittest.skip("Skipped for now")
    def test_sender_email(self):
        driver = SeleniumDriver(self.driver)
        send_email_input = "//*[@id='emailSettings']/div[1]/p[2]/input"
        invalid_emails = ['test@@test.com', 'test@test..com',
                          '@.com', 'test', 'test.com', 'test@t.c', '']

        self.open_email_settings()
        time.sleep(3)
        self.default_ip_email_rep()
        time.sleep(3)

        for email in invalid_emails:
            driver.wait_until_clickable(send_email_input, XPATH)
            driver.send_input(send_email_input, XPATH, email)
            driver.wait_and_click(save_btn(), XPATH)

            assert self.has_error(send_email_input) == True
            assert self.is_hidden_string(notify_msg()) == False

            driver.element_click("btnOk", ID)
        driver.wait_and_click(cancel_btn(), XPATH)

        time.sleep(3)
        self.restore_email_settings()

    @unittest.skip("Skipped for now")
    def test_port_number(self):
        driver = SeleniumDriver(self.driver)
        port_input = "//*[@id='emailSettings']/div[1]/p[3]/input"
        invalid_ports = ['test', 'test123', '---']

        self.open_email_settings()
        time.sleep(3)
        self.default_ip_email_rep()
        time.sleep(3)

        for port in invalid_ports:
            driver.wait_until_clickable(port_input, XPATH)
            driver.send_input(port_input, XPATH, port)
            driver.wait_and_click(save_btn(), XPATH)

            assert self.has_error(port_input) == True
            assert self.is_hidden_string(notify_msg()) == False

            driver.element_click("btnOk", ID)
        driver.wait_and_click(cancel_btn(), XPATH)

        time.sleep(3)
        self.restore_email_settings()

    @unittest.skip("Skipped for now")
    def test_authentication(self):
        driver = SeleniumDriver(self.driver)
        username = "//*[@id='emailSettings']/div[2]/p[2]/input"
        password = "//*[@id='emailSettings']/div[2]/p[3]/input[1]"
        confirmPass = "//*[@id='emailSettings']/div[2]/p[4]/input[1]"
        showPass = "//*[@id='emailSettings']/div[2]/p[5]/input"  # show password

        self.open_email_settings()
        self.default_ip_email_rep()
        time.sleep(3)

        driver.wait_and_click("authReq", ID)
        driver.wait_and_click(save_btn(), XPATH)

        assert self.has_error(username) == True
        assert self.has_error(password) == True
        assert self.has_error(confirmPass) == True
        assert self.is_hidden_string(notify_msg()) == False

        driver.element_click("btnOk", ID)

        time.sleep(3)
        driver.wait_for_visibility(password, XPATH)
        driver.get_element(password, XPATH)
        driver.send_input(password, XPATH, "Test123")

        driver.get_element(confirmPass, XPATH)
        driver.send_input(confirmPass, XPATH, "Test123")

        driver.element_click(showPass, XPATH)
        if driver.is_element_selected(showPass, XPATH):
            # if 'hidden' is in the password class
            assert self.is_hidden_string(password) == True

            time.sleep(3)
            driver.element_click(showPass, XPATH)

            # if 'hidden' is not in the password class
            assert self.is_hidden_string(password) == False

        driver.wait_and_click(cancel_btn(), XPATH)

        time.sleep(3)
        self.restore_email_settings()

    # @unittest.skip("Skipped for now")
    def test_recipients(self):
        driver = SeleniumDriver(self.driver)
        addRepBtn = "//*[@id='emailSettings']/div[3]/p[2]/button"  # add recipient button
        removeRepBox = "//*[@id='emailSettings']/div[3]/div[" \
                       "not(contains(@class, 'recpEntry hidden'))]/p[1]/b/span"
        send_email_btn = "//*[@id='emailSettings']/p/button"
        emailIpHost = "//*[@id='emailSettings']/div[1]/p[1]/input"
        send_email_input = "//*[@id='emailSettings']/div[1]/p[2]/input"

        self.open_email_settings()
        time.sleep(3)

        driver.send_input(emailIpHost, XPATH, "8.8.8.8")
        driver.send_input(send_email_input, XPATH, "test123t@middleatlantic.com")

        time.sleep(3)

        rep_div_count = 0  # number of "recpEntry" div
        i = 2
        for x in range(0, 5):
            repName = "//*[@id='emailSettings']/div[3]/div[{0}]/p[1]/input".format(i)
            repEmail = "//*[@id='emailSettings']/div[3]/div[{0}]/p[2]/input".format(i)
            time.sleep(2)
            driver.get_element(addRepBtn, XPATH)
            driver.wait_and_click(addRepBtn, XPATH)

            time.sleep(2)
            driver.send_input(repName, XPATH, "Test Test")
            driver.send_input(repEmail, XPATH, "test.test@middleatlantic.com")
            rep_div_count += 1

            i += 1

        assert rep_div_count == 5

        driver.wait_and_click(send_email_btn, XPATH)
        time.sleep(3)

        assert self.is_hidden_string(success_msg()) == False
        driver.wait_and_click(close_btn_msg(), XPATH)

        # get removeRepBoxList, length should be 5
        removeRepBoxList = self.driver.find_elements_by_xpath(removeRepBox)
        i = 2
        for x in removeRepBoxList:
            removeRepBox = "//*[@id='emailSettings']/div[3]/div[{0}]/p[1]/b/span".format(i)
            time.sleep(3)
            driver.wait_and_click(removeRepBox, XPATH)

        # get removeRepBoxList again, length should be 0
        removeRepBoxList = self.driver.find_elements_by_xpath(removeRepBox)

        assert len(removeRepBoxList) == 0

        driver.wait_and_click(cancel_btn(), XPATH)

        time.sleep(3)
        self.restore_email_settings()

    # -------------------- Functions --------------------------------

    def restore_email_settings(self):
        driver = SeleniumDriver(self.driver)
        factoryDefaults = "//nav/ul/li[5]"
        restoreEmailSett = "//*[@id='factoryDefaults']/p[7]/input"

        driver.wait_and_click(menu(), XPATH)
        time.sleep(3)
        driver.force_click(factoryDefaults, XPATH)

        time.sleep(3)
        driver.element_click(restoreEmailSett, XPATH)
        driver.wait_and_click(save_btn(), XPATH)

        time.sleep(11)  # wait for 10 seconds plus another second to click on OK button
        driver.element_click("btnOk", ID)

    def open_email_settings(self):
        menuIcon = ".//*[@id='wrapper']/header/i"
        emailSettings = "//nav/ul/li[4]"

        driver = SeleniumDriver(self.driver)
        driver.get_element(menuIcon, XPATH)
        driver.wait_and_click(menuIcon, XPATH)

        time.sleep(3)
        driver.force_click(emailSettings, XPATH)

    def default_ip_email_rep(self):
        driver = SeleniumDriver(self.driver)
        emailIpHost = "//*[@id='emailSettings']/div[1]/p[1]/input"
        senderEmail = "//*[@id='emailSettings']/div[1]/p[2]/input"
        addRepBtn = "//*[@id='emailSettings']/div[3]/p[2]/button"  # add recipient button
        repName = "//*[@id='emailSettings']/div[3]/div[2]/p[1]/input"
        repEmail = "//*[@id='emailSettings']/div[3]/div[2]/p[2]/input"
        recpEntry = "//*[@id='emailSettings']/div[3]/div[2]"

        if not driver.is_element_present(recpEntry, XPATH):
            driver.wait_and_click(addRepBtn, XPATH)
            time.sleep(3)

        driver.send_input(emailIpHost, XPATH, "12.12.12.12")
        driver.send_input(senderEmail, XPATH, "test@test.com")

        driver.send_input(repName, XPATH, "Test Test")
        driver.send_input(repEmail, XPATH, "test.test@middleatlantic.com")



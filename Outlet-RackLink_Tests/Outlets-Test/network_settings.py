# coding=utf-8

import time
import unittest
from Utils.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class NetworkSettings(TestFixtures):

    # -------------------- Tests --------------------------------

    #@unittest.skip("Skipped for now")
    def test_network(self):
        driver = SeleniumDriver(self.driver)
        DHCPCheckBox = "//*[@id='networkSettings']/div[3]/input"
        HTTPPort = "//*[@id='networkHttpPort']"
        network_ip_address = "//*[@id='networkIPAddress']"
        subnet_mask = "//*[@id='networkSettings']/p[2]/input"
        gateway = "//*[@id='networkSettings']/p[3]/input"
        dns_1 = ".//*[@id='networkSettings']/p[4]/input"
        dns_2 = "//*[@id='networkSettings']/p[5]/input"
        ipAddresses = ['0.8.8.8', '8.8.8.0', '255.8.8.8', '20.255.80',
                       '8.8.8', '8.8.8.8.8']

        self.open_network_settings()
        time.sleep(3)

        driver.send_input(HTTPPort, XPATH, "---")
        driver.wait_and_click(save_btn(), XPATH)

        assert self.is_hidden_string(notify_msg()) == False

        driver.wait_and_click("btnOk", ID)

        driver.wait_and_click(DHCPCheckBox, XPATH)

        for ip in ipAddresses:
            driver.wait_until_clickable(network_ip_address, XPATH)
            driver.send_input(network_ip_address, XPATH, ip)
            driver.send_input(subnet_mask, XPATH, ip)
            driver.send_input(gateway, XPATH, ip)
            driver.send_input(dns_1, XPATH, ip)
            driver.send_input(dns_2, XPATH, ip)
            driver.wait_and_click(save_btn(), XPATH)

            assert self.has_error(network_ip_address) == True
            assert self.is_hidden_string(notify_msg()) == False

            driver.element_click("btnOk", ID)
        driver.wait_and_click(cancel_btn(), XPATH)

        time.sleep(3)
        self.restore_network_settings()


    # -------------------- Functions --------------------------------

    def restore_network_settings(self):
        driver = SeleniumDriver(self.driver)
        menuIcon = ".//*[@id='wrapper']/header/i"
        factoryDefaults = "//nav/ul/li[5]"
        restore_network_def = "//*[@id='factoryDefaults']/p[10]/input"

        driver.wait_and_click(menuIcon, XPATH)
        time.sleep(3)
        driver.force_click(factoryDefaults, XPATH)

        time.sleep(3)
        driver.element_click(restore_network_def, XPATH)
        driver.wait_and_click(save_btn(), XPATH)

        time.sleep(11)  # wait for 10 seconds plus another second to click on OK button
        driver.element_click("btnOk", ID)

    def open_network_settings(self):
        network_settings = "//nav/ul/li[7]"

        driver = SeleniumDriver(self.driver)
        driver.get_element(menu(), XPATH)
        driver.wait_and_click(menu(), XPATH)

        time.sleep(3)
        driver.force_click(network_settings, XPATH)




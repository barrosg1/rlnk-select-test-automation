import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletIpAddressPing(TestFixtures):

    def test_ip_address_ping(self):
        """ Asserts that the ip address input value is valid
            test_operation.py contains all the functionality for each test
            Tests:
                '8.8.8.8' -> Valid IP address that works
                '0.8.8.8' -> Cannot start with 0
                '8.8.8.0' -> Cannot end with 0
                '255.8.8.8' -> Each node must be less than 255 and greater than 0
                '.8.8.8' -> A node cannot be empty
                '8.8.8' -> There must be exactly 4 nodes separated by dots (periods)
        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        enabledBtn = '//div[8]/div[2]/form[1]/button[2]'
        ipAddressInputElem = '//div[8]/div[2]/form[2]/p[1]/input'
        invalid_ips = ['0.8.8.8', '8.8.8.0', '255.8.8.8', '20.255.90',
                       '8.8.8', '8.8.8.8.8']

        index = 1
        for outletBox in outletBoxList:
            print "\n::::: Outlet " + str(index) + " :::::\n"
            time.sleep(5)
            outletBox.click()

            if self.is_on(enabledBtn) is False:
                driver.wait_and_click(enabledBtn, XPATH)

            driver.wait_until_clickable(enabledBtn, XPATH)
            driver.get_element(enabledBtn, XPATH)

            if self.is_on(enabledBtn):
                for ip in invalid_ips:
                    driver.wait_until_clickable(ipAddressInputElem, XPATH)
                    driver.send_input(ipAddressInputElem, XPATH, ip)

                    driver.wait_and_click(outlet_save_btn(), XPATH)

                    ipNumVal = driver.get_element_attribute(ipAddressInputElem, XPATH, VALUE)
                    nodes = ip_nodes(ipNumVal)

                    if self.is_hidden_string(notify_msg()) is False:
                        expectedOpGood = True

                        driver.element_click("btnOk", ID)
                        ipInputClass = driver.get_element_attribute(ipAddressInputElem, XPATH, ClASS)

                        if ip.startswith("0"):
                            assert starts_with_zero(ipNumVal, ipInputClass) == expectedOpGood
                        elif ip.endswith("0"):
                            assert ends_with_zero(ipNumVal, ipInputClass) == expectedOpGood
                        elif "255" in ip:
                            assert node_255(ipNumVal, ipInputClass) == expectedOpGood
                        elif len(nodes) < 4:
                            assert short_ip_node_length(ipNumVal, ipInputClass) == expectedOpGood
                        else:
                            assert long_ip_node_length(ipNumVal, ipInputClass) == expectedOpGood

                        time.sleep(1)

                    print "Testing: " + ip + " | has-error class appeared | " + "  PASSED"
                driver.send_input(ipAddressInputElem, XPATH, "8.8.8.8")
                driver.wait_and_click(outlet_save_btn(), XPATH)
                driver.wait_and_click(close_btn_msg(), XPATH)

            index += 1

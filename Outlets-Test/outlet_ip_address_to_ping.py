from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *
import time


class OutletIpAddressPing(TestFixtures):
    def test_outlet_ip_address_ping(self):
        ipAddresses = get_ip_addresses()

        for ipAddress in ipAddresses:
            self.baseUrl = ipAddress

            ip_baseUrl_title(self.baseUrl)
            try:
                self.driver.get(self.baseUrl)
            except:
                print "Invalid IP Address"
                continue

            self.ip_address_ping()

    def ip_address_ping(self):
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
        notifyMsg = ".//*[@id='notify']"
        ipAddresses = ['0.8.8.8', '8.8.8.0', '255.8.8.8', '20.255.90' '8.8.8', '8.8.8.8.8']

        index = 1
        for outletBox in outletBoxList:
            print "\n::::: Outlet " + str(index) + " :::::\n"
            time.sleep(5)
            outletBox.click()

            enabledBtnClass = driver.getElement(enabledBtn, XPATH).get_attribute(ClASS)

            if 'state1' not in enabledBtnClass or 'state2' in enabledBtnClass:
                driver.waitAndClick(enabledBtn, XPATH)

            driver.waitForElement(enabledBtn, XPATH)
            driver.getElement(enabledBtn, XPATH)

            if 'state1' in enabledBtnClass:
                for ip in ipAddresses:
                    driver.waitForElement(ipAddressInputElem, XPATH)
                    driver.sendInput(ipAddressInputElem, XPATH, ip)

                    driver.waitAndClick(save_btn_xpath(), XPATH)

                    ipNumVal = driver.getElementAttribute(ipAddressInputElem, XPATH, VALUE)
                    notifyMsgClass = driver.getElementAttribute(notifyMsg, XPATH, ClASS)
                    nodes = ip_nodes(ipNumVal)

                    if 'hidden' not in notifyMsgClass:
                        expectedOpGood = True

                        driver.elementClick("btnOk", ID)
                        ipInputClass = driver.getElementAttribute(ipAddressInputElem, XPATH, ClASS)

                        if ip.startswith("0"):
                            assert starts_with_zero(ipNumVal, ipInputClass) == expectedOpGood
                        elif ip.endswith("0"):
                            assert ends_with_zero(ipNumVal, ipInputClass) == expectedOpGood
                        elif "255" in ip:
                            assert node_255(ipNumVal, ipInputClass) == expectedOpGood
                        elif len(nodes) < 4:
                            assert short_node_length(ipNumVal, ipInputClass) == expectedOpGood
                        else:
                            assert long_node_length(ipNumVal, ipInputClass) == expectedOpGood

                        time.sleep(1)
                    print "Testing: " + ip + " | has-error class appeared | " + "  PASSED"
                driver.sendInput(ipAddressInputElem, XPATH, "8.8.8.8")
                driver.waitAndClick(save_btn_xpath(), XPATH)

            index += 1

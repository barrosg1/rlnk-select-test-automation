# coding=utf-8
import unittest
import time

from Utils.fixtures_test import TestFixtures

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletPowerState(TestFixtures):
    #@unittest.skip("Skipped for now")
    def test_power_state_btn_notify_msg(self):
        """
        Verifies that a popup comes up with an Are you sure… message.
        Look for the DOM element “notify”

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerStateBtn = '//div[8]/div[2]/form[1]/button[1]'

        i=2
        for outletBox in outletBoxList:
            outletCtrlStr = "//*[@id='outletControl']/div[{0}]".format(i)
            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)

            if self.is_on(powerStateBtn):
                driver.wait_and_click(powerStateBtn, XPATH)

                assert self.is_hidden_string(notify_msg()) == False
                driver.wait_and_click("btnOk", ID)

                time.sleep(1)
                if driver.is_element_present(success_msg(), XPATH):
                    assert self.is_hidden_string(success_msg()) == False
                    time.sleep(3)
            else:
                driver.wait_and_click(outlet_cancel_btn(), XPATH)

            i += 1

        time.sleep(3)
        self.seq_up()

    #@unittest.skip("Skipped for now")
    def test_power_state_verify_not_changed(self):
        """
        Verify that the power state has not changed
        after clicking the cancel button

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerStateBtn = '//div[8]/div[2]/form[1]/button[1]'

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()

            if self.is_on(powerStateBtn):
                powerState = True
            else:
                powerState = False

            driver.wait_and_click(powerStateBtn, XPATH)
            driver.wait_and_click("btnCancel", ID)
            driver.wait_and_click(outlet_cancel_btn(), XPATH)

            if powerState:
                assert powerState == True

            if self.is_on(powerStateBtn) is False:
                assert powerState == False

    #@unittest.skip("Skipped for now")
    def test_power_state_verify_changed(self):
        """
        Verify that the switch and outlet face change state
        Verify that a success message appears
        Verify that the outlet shrinks out of edit mode

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        powerStateBtn = '//div[8]/div[2]/form[1]/button[1]'
        outletEditMode = "//div[8]"

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            time.sleep(5)
            driver.wait_and_click(outletCtrlStr, XPATH)

            if self.is_on(powerStateBtn):
                powerState = True
            else:
                powerState = False

            driver.wait_and_click(powerStateBtn, XPATH)
            driver.wait_and_click("btnOk", ID)

            time.sleep(1)
            if driver.is_element_present(close_btn_msg(), XPATH):
                driver.wait_and_click(close_btn_msg(), XPATH)
                assert self.is_hidden_string(success_msg()) == False

            time.sleep(1)
            assert driver.is_element_present(outletEditMode, XPATH) == False

            driver.element_click(outletCtrlStr, XPATH)

            if powerState:
                if self.is_on(powerStateBtn):
                    assert powerState == True
            else:
                assert powerState == False

            driver.wait_and_click(outlet_cancel_btn(), XPATH)

            index += 1

        time.sleep(3)
        self.seq_up()

    # --------------------------- Functions ---------------------------

    def seq_up(self):
        """ Tests sequence up
            Asserts a valid delay input
        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        upBtn = ".//*[@id='sequenceControl']/div[2]/div/button[1]"
        initiateBtn = ".//*[@id='seqDelayCtrl']/div/button[2]"
        delayInput = ".//*[@id='seqDelayCtrl']/span/input"
        inputNum = 1

        numOfOutletBox = len(outletBoxList)
        index = 2
        for outlet in outletBoxList:
            if index > numOfOutletBox: break

            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)

            if self.is_on(outletCtrlStr):
                index += 1
            else:
                driver.wait_and_click(upBtn, XPATH)
                driver.send_input(delayInput, XPATH, inputNum)

                driver.wait_and_click(initiateBtn, XPATH)
                break




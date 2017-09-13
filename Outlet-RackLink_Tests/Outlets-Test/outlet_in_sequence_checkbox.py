# coding=utf-8
import unittest
import time

from Utils.fixtures_test import TestFixtures
from selenium.webdriver.common.action_chains import ActionChains

from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *


class OutletInSequence(TestFixtures):
    @unittest.skip("Skipped for now")
    def test_inSeq_selected(self):
        """
        Asserts each outlet is in-sequence
        This function clicks on each outlet and make sure the check
        box is checked. If it is already checked, then it continues to the next
        outlet
        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        inSeqInput = "//div[8]/div[2]/form[1]/p[1]/input"
        outletsWithStateOff = self.driver.find_elements_by_class_name("state-off")

        numOfOutletBox = len(outletBoxList)
        numOutletsStateOff = len(outletsWithStateOff)

        if numOutletsStateOff == numOfOutletBox:
            assert numOutletsStateOff == numOfOutletBox
            print "\nAll outlets are already off"
            return

        outletCount = 1
        for outletBox in outletBoxList:
            outlet_count(outletCount)
            time.sleep(5)
            outletBox.click()
            time.sleep(3)

            if not driver.is_element_selected(inSeqInput, XPATH):
                driver.element_click(inSeqInput, XPATH)
                assert driver.is_element_selected(inSeqInput, XPATH) == True
                driver.wait_and_click(outlet_save_btn(), XPATH)
            else:
                driver.wait_and_click(outlet_save_btn(), XPATH)

            if 'in-sequence' in outletBox.get_attribute(ClASS):
                assert 'in-sequence' in outletBox.get_attribute(ClASS)

            outletCount += 1

        time.sleep(8)

    @unittest.skip("Skipped for now")
    def test_check_inSeq_only(self):
        """
        Verify that the outlet is no longer displayed in the Outlet Control
        section with the “Show in Sequence Outlets Only”
        Verify “There are currently no outlets which are set with in
        sequence setting checked" pops up

        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        inSeqOnlyOption = "//*[@id='ocFilter']/option[contains(@value, 'sequenced')]"
        inSeqInput = "//div[8]/div[2]/form[1]/p[1]/input[contains(@type, 'checkbox')]"
        clickAway = ".//*[@id='outletControl']/h1"

        time.sleep(3)
        driver.wait_and_click("ocFilter", ID)

        time.sleep(3)
        driver.wait_and_click(inSeqOnlyOption, XPATH)
        driver.wait_and_click(clickAway, XPATH)

        time.sleep(2)
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            if not outletBox.is_displayed():
                continue

            time.sleep(5)
            outletBox.click()

            driver.wait_and_click(inSeqInput, XPATH)
            driver.wait_and_click(outlet_save_btn(), XPATH)

            time.sleep(8)
            outletDisplayed = self.driver.find_element_by_xpath(outletCtrlStr).is_displayed()
            if not outletDisplayed:
                assert outletDisplayed == False
                print "Outlet is no longer in-sequence |  PASSED"

            index += 1

        theMsgDisplayed = self.driver.find_element_by_xpath(notify_msg()).is_displayed()
        if theMsgDisplayed:
            driver.wait_and_click("btnOk", ID)

        assert theMsgDisplayed == True
        print '"Currently no outlets in in-seq" message displayed |  PASSED '

        time.sleep(8)

    @unittest.skip("Skipped for now")
    def test_seq_down(self):
        """ Tests sequence down
            Asserts a valid delay input
        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        outletsWithStateOff = self.driver.find_elements_by_class_name("state-off")

        downBtn = ".//*[@id='sequenceControl']/div[2]/div/button[2]"
        initiateBtn = ".//*[@id='seqDelayCtrl']/div/button[2]"
        delayInput = ".//*[@id='seqDelayCtrl']/span/input"
        inputNum = 3

        numOfOutletBox = len(outletBoxList)
        numOutletsStateOff = len(outletsWithStateOff)

        self.restore_seq_defaults()

        time.sleep(4)
        if numOutletsStateOff == numOfOutletBox:
            assert numOutletsStateOff == numOfOutletBox
            print "\nAll outlets are already off"
            return
        else:
            index = numOfOutletBox
            for outlet in outletBoxList[::-1]:
                outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)

                if self.is_on(outletCtrlStr) is False:
                    index -= 1
                else:
                    driver.wait_and_click(downBtn, XPATH)
                    driver.send_input(delayInput, XPATH, inputNum)

                    delayInputVal = driver.get_element_attribute(delayInput, XPATH, VALUE)
                    assert 255 >= int(delayInputVal) >= 1
                    print "Delay input value is within 1 - 255 |  PASSED"

                    driver.wait_and_click(initiateBtn, XPATH)
                    break
            time.sleep(inputNum * numOfOutletBox)

        outletsWithStateOff = self.driver.find_elements_by_class_name("state-off")
        numOutletsStateOff = len(outletsWithStateOff)
        assert numOutletsStateOff == numOfOutletBox

    # @unittest.skip("Skipped for now")
    def test_seq_up(self):
        """ Tests sequence up
            Asserts a valid delay input
        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        upBtn = ".//*[@id='sequenceControl']/div[2]/div/button[1]"
        initiateBtn = ".//*[@id='seqDelayCtrl']/div/button[2]"
        delayInput = ".//*[@id='seqDelayCtrl']/span/input"
        inputNum = 5

        outletsWithStateOn = self.driver.find_elements_by_class_name("state-on")
        numOfOutletBox = len(outletBoxList)
        numOutletsStateOn = len(outletsWithStateOn)

        if numOutletsStateOn == numOfOutletBox:
            assert numOutletsStateOn == numOfOutletBox
            print "\nAll the outlets are already on"
            return
        else:
            index = 2
            for outlet in outletBoxList:
                if index > numOfOutletBox: break

                outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)

                if self.is_on(outletCtrlStr):
                    index += 1
                else:
                    driver.wait_and_click(upBtn, XPATH)
                    driver.send_input(delayInput, XPATH, inputNum)

                    delayInputVal = driver.get_element_attribute(delayInput, XPATH, VALUE)
                    assert 255 >= int(delayInputVal) >= 1
                    print "Delay input value is withing 1 - 255 |  PASSED"

                    driver.wait_and_click(initiateBtn, XPATH)
                    break

        time.sleep(inputNum * numOfOutletBox)

        outletsWithStateOn = self.driver.find_elements_by_class_name("state-on")
        numOutletsStateOn = len(outletsWithStateOn)
        assert numOutletsStateOn == numOfOutletBox
        print "All visible outlets turned on |  PASSED"

    # ------------------------- Functions ------------------------------

    def restore_seq_defaults(self):
        """ This function will set the in sequence checkbox of all of the outlets """

        driver = SeleniumDriver(self.driver)
        menuIcon = ".//*[@id='wrapper']/header/i"
        factoryDefaults = "//nav/ul/li[5]"
        restoreSeqDef = "//*[@id='factoryDefaults']/p[9]/input"

        driver.wait_and_click(menuIcon, XPATH)
        time.sleep(3)
        driver.force_click(factoryDefaults, XPATH)

        time.sleep(3)

        driver.element_click(restoreSeqDef, XPATH)
        driver.wait_and_click(save_btn(), XPATH)

        time.sleep(11)
        driver.element_click("btnOk", ID)

# coding=utf-8
from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from Utils.string_constants import *
from Utils.test_operation import *
import sys
import time


class OutletInSequence(TestFixtures):
    def test_outlet_in_sequence(self):
        ipAddresses = get_ip_addresses()

        for ipAddress in ipAddresses:
            self.baseUrl = ipAddress

            ip_baseUrl_title(self.baseUrl)
            try:
                self.driver.get(self.baseUrl)
            except:
                print "Invalid IP Address"
                continue

            self.inSeq_selected()
            self.check_inSeq_only()
            self.seq_down()
            self.seq_up()

    # --------------------------------------------------------------

    def restore_seq_defaults(self):
        """ This function will set the in sequence checkbox of all of the outlets """

        driver = SeleniumDriver(self.driver)
        menuIcon = ".//*[@id='wrapper']/header/i"
        factoryDefaults = "//nav/ul/li[5]"
        restoreSeqDef = "//*[@id='factoryDefaults']/p[9]/input"
        saveBtn = ".//*[@id='spbg']/button[2]"

        driver.waitAndClick(menuIcon, XPATH)
        time.sleep(3)
        elem = driver.getElement(factoryDefaults, XPATH)
        actions = ActionChains(self.driver)
        actions.move_to_element(elem)
        actions.click(elem)
        actions.perform()

        time.sleep(3)

        driver.elementClick(restoreSeqDef, XPATH)
        driver.waitAndClick(saveBtn, XPATH)

        time.sleep(11)
        driver.elementClick("btnOk", ID)

    def inSeq_selected(self):
        """
        Asserts each outlet is in-sequence
        This function clicks on each outlet and make sure the check
        box is checked. If it is already checked, then it continues to the next
        outlet
        """

        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

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

            if not driver.isElementSelected(inSeqInput, XPATH):
                driver.elementClick(inSeqInput, XPATH)
                assert driver.isElementSelected(inSeqInput, XPATH) == True
                driver.waitAndClick(outlet_save_btn(), XPATH)
            else:
                driver.waitAndClick(outlet_save_btn(), XPATH)

            if 'in-sequence' in outletBox.get_attribute(ClASS):
                assert 'in-sequence' in outletBox.get_attribute(ClASS)

            outletCount += 1

        time.sleep(8)

    def check_inSeq_only(self):
        """
        Verify that the outlet is no longer displayed in the Outlet Control
        section with the “Show in Sequence Outlets Only”
        Verify “There are currently no outlets which are set with in
        sequence setting checked" pops up

        """

        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        inSeqOnlyOption = "//*[@id='ocFilter']/option[contains(@value, 'sequenced')]"
        inSeqInput = "//div[8]/div[2]/form[1]/p[1]/input[contains(@type, 'checkbox')]"
        clickAway = ".//*[@id='outletControl']/h1"
        theMsg = ".//*[@id='notify']/div"

        time.sleep(3)
        driver.waitAndClick("ocFilter", ID)

        time.sleep(3)
        driver.waitAndClick(inSeqOnlyOption, XPATH)
        driver.waitAndClick(clickAway, XPATH)

        time.sleep(2)
        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            if not outletBox.is_displayed():
                continue

            time.sleep(5)
            outletBox.click()

            driver.waitAndClick(inSeqInput, XPATH)
            driver.waitAndClick(outlet_save_btn(), XPATH)

            time.sleep(8)
            outletDisplayed = self.driver.find_element_by_xpath(outletCtrlStr).is_displayed()
            if not outletDisplayed:
                assert outletDisplayed == False
                print "Outlet is no longer in-sequence |  PASSED"

            index += 1

        theMsgDisplayed = self.driver.find_element_by_xpath(theMsg).is_displayed()
        if theMsgDisplayed:
            driver.waitAndClick("btnOk", ID)

        assert theMsgDisplayed == True
        print '"Currently no outlets in in-seq" message displayed |  PASSED '

        time.sleep(8)

    def seq_down(self):
        """ Tests sequence down
            Asserts a valid delay input
        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

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
                outletCtrlClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)

                if "state-off" in outletCtrlClass:
                    index -= 1
                else:
                    driver.waitAndClick(downBtn, XPATH)
                    driver.sendInput(delayInput, XPATH, inputNum)

                    delayInputVal = driver.getElementAttribute(delayInput, XPATH, VALUE)
                    assert 255 >= int(delayInputVal) >= 1
                    print "Delay input value is within 1 - 255 |  PASSED"

                    driver.waitAndClick(initiateBtn, XPATH)
                    break
            time.sleep(inputNum * numOfOutletBox)

        outletsWithStateOff = self.driver.find_elements_by_class_name("state-off")
        numOutletsStateOff = len(outletsWithStateOff)
        assert numOutletsStateOff == numOfOutletBox

    def seq_up(self):
        """ Tests sequence up
            Asserts a valid delay input
        """
        print "Test case function: " + "(" + sys._getframe().f_code.co_name + ")"

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
                outletCtrlClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)

                if "state-on" in outletCtrlClass:
                    index += 1
                else:
                    driver.waitAndClick(upBtn, XPATH)
                    driver.sendInput(delayInput, XPATH, inputNum)

                    delayInputVal = driver.getElementAttribute(delayInput, XPATH, VALUE)
                    assert 255 >= int(delayInputVal) >= 1
                    print "Delay input value is withing 1 - 255 |  PASSED"

                    driver.waitAndClick(initiateBtn, XPATH)
                    break

        time.sleep(inputNum * numOfOutletBox)

        outletsWithStateOn = self.driver.find_elements_by_class_name("state-on")
        numOutletsStateOn = len(outletsWithStateOn)
        assert numOutletsStateOn == numOfOutletBox
        print "All visible outlets turned on |  PASSED"

from Config.fixtures_test import TestFixtures
from Utils.selenium_driver import SeleniumDriver
from Utils.string_constants import *
from Utils.test_operation import *
import time
from selenium.webdriver.common.keys import Keys


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

            self.restore_seq_defaults()
            # self.inSeq_selected()
            # self.check_inSeq_only()

            # self.seq_down()
            # self.seq_up()

    # --------------------------------------------------------------

    def restore_seq_defaults(self):
        driver = SeleniumDriver(self.driver)
        menuIcon = ".//*[@id='wrapper']/header/i"
        factoryDefaults = "//li[5]"
        restoreSeqDef = ".//*[@id='factoryDefaults']/p[9]/input"
        saveBtn = ".//*[@id='spbg']/button[2]"

        driver.waitAndClick(menuIcon, XPATH)
        driver.waitForElement(factoryDefaults, XPATH)

        listArray = []

        for item in self.driver.find_elements_by_xpath("//nav/ul"):
            listArray.append(item)

        for item in listArray:
            item.click()

        driver.waitForElement(restoreSeqDef, XPATH)
        driver.elementClick(saveBtn, XPATH)


    def inSeq_selected(self):
        """
        Asserts each outlet is in-sequence
        This function clicks on each outlet and make sure the check
        box is checked. If it is already checked, then it continues to the next
        outlet
        """

        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        inSeqInput = "//div[8]/div[2]/form[1]/p[1]/input[contains(@type, 'checkbox')]"
        outletsWithStateOff = self.driver.find_elements_by_class_name("state-off")

        numOfOutletBox = len(outletBoxList)
        numOutletsStateOff = len(outletsWithStateOff)

        if numOutletsStateOff == numOfOutletBox:
            assert numOutletsStateOff == numOfOutletBox
            print "\nAll outlets are already off"
            self.seq_up()
            return

        for outletBox in outletBoxList:
            time.sleep(5)
            outletBox.click()
            driver.waitForElement(inSeqInput, XPATH)

            if not driver.isElementSelected(inSeqInput, XPATH):
                driver.elementClick(inSeqInput, XPATH)
                assert driver.isElementSelected(inSeqInput, XPATH) == True
                driver.elementClick(save_btn_xpath(), XPATH)
            else:
                driver.waitAndClick(save_btn_xpath(), XPATH)

            if 'in-sequence' in outletBox.get_attribute(ClASS):
                assert 'in-sequence' in outletBox.get_attribute(ClASS)

        time.sleep(8)


    def check_inSeq_only(self):
        driver = SeleniumDriver(self.driver)
        outletBoxList = self.driver.find_elements_by_xpath(outlet_box_xpath())
        inSeqOnlyOption = "ocFilter"
        inSeqInput = "//div[8]/div[2]/form[1]/p[1]/input[contains(@type, 'checkbox')]"

        driver.waitAndClick(inSeqOnlyOption, ID)

        time.sleep(3)
        driver.elementClick(".//*[@id='ocFilter']/option[2]", XPATH)
        driver.waitAndClick(".//*[@id='outletControl']/h1", XPATH)

        index = 2
        for outletBox in outletBoxList:
            outletCtrlStr = ".//*[@id='outletControl']/div[{0}]/div[1]".format(index)
            outletClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)
            if 'hidden' in outletClass:
                continue
            time.sleep(5)
            outletBox.click()
            driver.waitForElement(inSeqInput, XPATH)

            if driver.isElementSelected(inSeqInput, XPATH):
                driver.waitAndClick(inSeqInput, XPATH)
                driver.waitAndClick(save_btn_xpath(), XPATH)

            time.sleep(8)
            driver.waitForElement(outletCtrlStr, XPATH)
            driver.getElement(outletCtrlStr, XPATH)

            if driver.isElementPresent(outletCtrlStr, XPATH):
                print "Element is present"
            else:
                print "Element is not present"


            index += 1
        time.sleep(8)

    def seq_down(self):
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

                    assert int(delayInputVal) == inputNum
                    assert 255 >= int(delayInputVal) >= 1

                    driver.waitAndClick(initiateBtn, XPATH)
                    break
            time.sleep(inputNum * 2)

    def seq_up(self):
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
                outletCtrlClass = driver.getElementAttribute(outletCtrlStr, XPATH, ClASS)

                if "state-on" in outletCtrlClass:
                    index += 1
                else:
                    driver.waitAndClick(upBtn, XPATH)
                    driver.sendInput(delayInput, XPATH, inputNum)

                    delayInputVal = driver.getElementAttribute(delayInput, XPATH, VALUE)

                    assert int(delayInputVal) == inputNum
                    assert 255 >= int(delayInputVal) >= 1

                    driver.waitAndClick(initiateBtn, XPATH)
                    break
        time.sleep(inputNum * 2)
"""
All functions return a string that will be used to find one or more element(s)
(these are commonly used locators throughout the program)

"""

ID = 'id'
XPATH = 'xpath'
CSS = 'css'
ClASS = 'class'
VALUE = 'value'


def outlet_box_xpath():
    """
    function is used to return a the xpath of visible outlets
    elem returns all the outlet boxes that is NOT hidden.
    The first outlet box IS hidden
    index starts at 1 (but index 1 is hidden), so visible outlet box starts at index [2]

    """

    elem = "//*[@id='outletControl']/div[not(contains(@class, 'infoBox hidden'))]"
    return elem


def outlet_save_btn():
    """ returns the save button xpath """
    elem = "//div[8]/div[2]/div/button[contains(@class, 'saveBtn')]"
    return elem


def outlet_cancel_btn():
    """ return the cancel button xpath """
    elem = "//div[8]/div[2]/div/button[1]"
    return elem

def save_btn():
    elem = "//*[@id='spbg']/button[2]"
    return elem

def cancel_btn():
    elem = "//*[@id='spbg']/button[1]"
    return elem

def success_msg():
    elem = "//*[@id='successMsg']"
    return elem

def close_btn_msg():
    """ return the success message close button xpath """
    elem = "//*[@id='closeBtn6']/span"
    return elem


def notify_msg():
    elem = "//*[@id='notify']"
    return elem

def menu():
    elem = ".//*[@id='wrapper']/header/i"
    return elem


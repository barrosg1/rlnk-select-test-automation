"""
All functions return a string that will be used to find an element

"""
ID = 'id'
XPATH = 'xpath'
ClASS = 'class'
VALUE = 'value'

def outlet_box_xpath():
    elem = "//*[@id='outletControl']/div[not(contains(@class, 'infoBox hidden'))]"
    return elem


def save_btn_xpath():
    elem = "//div[8]/div[2]/div/button[2]"
    return elem


def cancel_btn_xpath():
    elem = "//div[8]/div[2]/div/button[1]"
    return elem


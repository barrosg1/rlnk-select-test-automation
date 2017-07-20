import unittest
from selenium import webdriver
import time

class TestFixtures(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        print "\nTest Complete"
        time.sleep(5)
        self.driver.quit()

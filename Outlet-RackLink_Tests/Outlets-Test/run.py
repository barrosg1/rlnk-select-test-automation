"""
There are two ways to run the test suite:

1) run using TextTestRunner class to see results on the command line
2) run using HTMLTestRunner class to see results in HTML

To add another test to the suite, simply import the test class and append it to the tests array

"""

import unittest
from unittest import TestLoader, TestSuite
from Config import HTMLTestRunner
import datetime
from Utils.test_operation import *

# -------- TestCase classes import -------------
from outlet_name_change import OutletNameChange
from outlet_powerstate_change import OutletPowerState
from outlet_in_sequence_checkbox import OutletInSequence
from outlet_auto_ping import OutletAutoPing
from outlet_cycle_delay import OutletCycleDelay
from outlet_edit_cancel_func import OutletEditCancel
from outlet_ip_address_to_ping import OutletIpAddressPing
from outlet_retries_test import OutletRetries
from outlet_frequency_test import OutletFrequency
from outlet_recovery_action import OutletRecoveryAction
from outlet_date_time import OutletDateTime
from outlet_device_settings import OutletDeviceSettings
from outlet_email_settings import OutletEmailSettings

if __name__ == "__main__":

    # Create a test list
    tests = [
        # OutletNameChange,
        # OutletInSequence
        # OutletAutoPing,
        # OutletCycleDelay,
        # OutletEditCancel,
        # OutletIpAddressPing
        # OutletRetries,
        # OutletFrequency
        # OutletPowerState
        # OutletRecoveryAction
        # OutletDateTime,
        # OutletDeviceSettings
        OutletEmailSettings
    ]

    # Load test cases
    loader = TestLoader()

    # Create a SuiteCase
    test_list = []
    for test in tests:
        cases = loader.loadTestsFromTestCase(test)
        test_list.append(cases)

    suite = TestSuite(test_list)

    # Run the suite
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    # -----------------------------------------------------------------------------------------------------

    """
       
    file_name = datetime.datetime.now().strftime("HTML_Reports/%Y_%m_%d_%H%M_RackLink-Select-Report.html")
l
    output = open(file_name, "wb")

    tests = [
        OutletNameChange,
        OutletRetries,
        OutletInSequence,
        OutletAutoPing,
        OutletCycleDelay,
        OutletEditCancel,
        OutletIpAddressPing,
        OutletFrequency,
        OutletPowerState
    ]

    loader = TestLoader()

    test_list = []
    for test in tests:
        cases = loader.loadTestsFromTestCase(test)
        test_list.append(cases)

    suite = TestSuite(test_list)

    runner = HTMLTestRunner.HTMLTestRunner(stream=output, verbosity=2, title="RackLink Select Automated Test Results")
    runner.run(suite)
    
    """

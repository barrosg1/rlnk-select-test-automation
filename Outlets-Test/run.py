import unittest
from unittest import TestLoader, TestSuite
from Config import HTMLTestRunner
import datetime

# TestCase classes import
from outlet_name_change import OutletNameChange
from outlet_powerstate_change import OutletPowerState
from outlet_in_sequence_checkbox import OutletInSequence
from outlet_auto_ping import OutletAutoPing
from outlet_cycle_delay import OutletCycleDelay
from outlet_edit_cancel_func import OutletEditCancel
from outlet_ip_address_to_ping import OutletIpAddressPing

if __name__ == "__main__":

    # Create a test list
    tests = [
        # OutletNameChange,
        # OutletPowerState,
        # OutletInSequence
        # OutletAutoPing,
        OutletCycleDelay,
        # OutletEditCancel,
        # OutletIpAddressPing
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

    output = open(file_name, "wb")

    tests = [
        #OutletNameChange,
        #OutletPowerState,
        #OutletInSequence,
        #OutletAutoPing,
        OutletCycleDelay,
        #OutletEditCancel,
        #OutletIpAddressPing
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

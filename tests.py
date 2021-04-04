import unittest

import bank_app.tests
from test_main import TestMain

all_tests = unittest.TestSuite([
        bank_app.tests.tests,
        unittest.TestLoader().loadTestsFromTestCase(TestMain),
    ])


def test_package():
    runner = unittest.TextTestRunner()
    print(runner.run(all_tests))


if __name__ == '__main__':
    test_package()

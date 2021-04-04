import unittest

from bank_app.tests.test_account import TestAccount
from bank_app.tests.test_operation import TestOperation


tests = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestAccount),
        unittest.TestLoader().loadTestsFromTestCase(TestOperation),
    ])


def test_package():
    runner = unittest.TextTestRunner()
    print(runner.run(tests))


if __name__ == '__main__':
    test_package()

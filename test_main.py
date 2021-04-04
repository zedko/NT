import unittest
import io
import sys

from moneyed import Money

from main import deposit, withdraw
from bank_app import Account, settings


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        """Create an account with some balance"""
        self.acc = Account("Joe")
        self.acc.create_and_add_operation('deposit', 1000.50)
        redirected_stdout = io.StringIO()
        sys.stdout = redirected_stdout

    def tearDown(self) -> None:
        """
        Clears all operations and set balance to zero
        """
        self.acc.operations = []
        self.acc.current_balance = Money(0, settings.CURRENCY)
        sys.stdout = sys.__stdout__

    def test_deposit(self):
        """ Add some money to the acc"""
        self.assertRaises(SystemExit, deposit, ['--client', 'Joe', '--amount', 0.5])
        self.assertEqual(Money(1001, settings.CURRENCY), self.acc.current_balance)

    def test_withdraw(self):
        """ Remove some money from the acc"""
        self.assertRaises(SystemExit, withdraw, ['--client', 'Joe', '--amount', 1000])
        self.assertEqual(Money(0.5, settings.CURRENCY), self.acc.current_balance)


if __name__ == '__main__':
    unittest.main()

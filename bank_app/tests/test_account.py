import unittest

from moneyed import Money

from bank_app import Account
from bank_app import BalanceException
from bank_app import Operation
from bank_app import settings


class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.acc = Account('Joe')
        self.operations = [
            Operation('deposit', '20'),
            Operation('deposit', 0.1),
            Operation('deposit', 40),
            Operation('withdraw', '40'),
            Operation('withdraw', '0.1'),
            Operation('withdraw', '20'),
        ]

    def tearDown(self) -> None:
        """
        Clears all operations and set balance to zero
        """
        self.acc.operations = []
        self.acc.current_balance = Money(0, settings.CURRENCY)

    def test_one_client_has_one_account(self):
        joe_another_acc = Account('Joe')
        not_joes_acc = Account('Not Joe')
        self.assertIs(self.acc, joe_another_acc)
        self.assertIsNot(self.acc, not_joes_acc)

    def test_deposits_and_withdrawals(self):
        """ Check deposits and withdrawals with Operation classes"""
        for operation in self.operations:
            self.acc.add_operation(operation)
        self.assertEqual(self.acc.current_balance, Money(0, settings.CURRENCY))

    def test_withdrawal_restrictions(self):
        bad_operation = Operation('withdraw', '100500')
        self.assertRaises(BalanceException, self.acc.add_operation, bad_operation)

    def test_create_and_add_operation(self):
        test_acc = Account("Simple Operation")
        test_acc.create_and_add_operation('deposit', 125.5)
        test_acc.create_and_add_operation('withdraw', '125.5', 'Description')
        self.assertEqual(test_acc.current_balance, Money(0, settings.CURRENCY))


if __name__ == '__main__':
    unittest.main()

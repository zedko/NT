import unittest

from moneyed import Money

from bank_app import Operation
from bank_app import settings


class TestOperation(unittest.TestCase):
    def test_creation(self):
        o = Operation('deposit', 100)
        self.assertIsInstance(o, Operation)
        self.assertEqual(o.amount, Money(100, settings.CURRENCY))

    def test_incorrect_amount(self):
        self.assertRaises(ValueError, Operation, 'deposit', -120)
        self.assertRaises(ValueError, Operation, 'deposit', '135/-5')

    def test_incorrect_operation_type(self):
        self.assertRaises(ValueError, Operation, '12345Blabla', 150)


if __name__ == '__main__':
    unittest.main()

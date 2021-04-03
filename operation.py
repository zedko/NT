from datetime import datetime
from typing import Union
from functools import partial

from moneyed import Money
from moneyed.l10n import format_money

# Hardcoded due to task restrictions
p_format_money = partial(format_money, locale='en_US')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CURRENCY = 'USD'


class Operation:
    """
    Represents any single bank operation
    """

    def __init__(self, operation: str, amount: Union[str, int, float], description: str = None):
        """
        :param operation: Type of operation. could be 'deposit' or 'withdraw'
        :param amount: Amount of money. Stored as Money type. Tt is best to avoid passing float type to __init__
        :param description: Description of the operation
        """
        self.currency = CURRENCY
        self.date = datetime.now()

        self._operation = self._set_operation(operation)
        self._amount = self._set_amount(amount)
        self._amount_formatted = p_format_money(self._amount)
        self.description = description or self._operation

    def __repr__(self) -> str:
        string = f"date: {self.date.strftime(DATE_FORMAT)} | type: {self.operation} | amount: {self._amount_formatted} "
        return string

    def get_table_row(self) -> list:
        """
        Forms a list for future rendering
        :return: list of strings
        """
        date = self.date.strftime(DATE_FORMAT)
        withdrawals = self._amount_formatted if self._operation == 'withdraw' else ""
        deposits = self._amount_formatted if self._operation == 'deposit' else ""

        return [date, self.description, withdrawals, deposits]

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, operation: str):
        raise AttributeError("Operation's type cannot be changed")

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        raise AttributeError("Operation's amount cannot be changed")

    def _set_amount(self, amount: Union[str, int, float]) -> Money:
        """
        Converts amount into Money type. Should be called once. At __init__
        :param amount: Amount of money. Must be positive
        :return: Money type
        """
        try:
            new_value = Money(amount=amount, currency=self.currency)
            if new_value <= Money(0, currency=self.currency):
                raise ValueError
            return new_value
        except Exception:
            raise ValueError(f'Cannot register Money operation with amount {amount}.'
                             f' Provide correct positive value of [str, int, float]')

    def _set_operation(self, operation: str):
        operation = operation.lower()
        available_operations = ['deposit', 'withdraw']
        if operation not in available_operations:
            raise ValueError(f'Operation type is not supported. Try one of {available_operations}')
        else:
            return operation


if __name__ == '__main__':
    a = Operation('deposit', 100)
    b = Operation('withdraw', '123.3', description="ATM Withdraw")
    print(a)
    print(b.get_table_row())

from collections import deque
from functools import partial
from datetime import datetime

from moneyed import Money
from moneyed.l10n import format_money
from prettytable import PrettyTable, ALL

from operation import Operation

# Hardcoded due to task restrictions
p_format_money = partial(format_money, locale='en_US')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CURRENCY = 'USD'


class BalanceException(Exception):
    """
    Raise when something wrong with Account balance
    """
    pass


class OneAccountPerClientMeta(type):
    """
    Metaclass that insures one client has only one account
    """
    _instances = {}

    def __call__(cls, client, *args, **kwargs):
        try:
            return cls._instances[client]
        except KeyError:
            cls._instances[client] = super().__call__(client, *args, **kwargs)
            return cls._instances[client]


class Account(metaclass=OneAccountPerClientMeta):
    """
    Represents bank account for a client
    """

    def __init__(self, client: str):
        self.currency = CURRENCY
        self.client = client
        self.current_balance = Money(0, self.currency)
        self.operations = deque()

    def __str__(self):
        return str(self.client)

    def add_operation(self, operation: Operation):
        """Adds and Operation to Account"""
        new_balance = self.change_balance(self.current_balance, operation)
        if new_balance >= Money(0, self.currency):
            self.operations.append(operation)
            self.current_balance = new_balance
        else:
            raise BalanceException(f'Not enough money to proceed operation')

    def show_bank_statement(self, since: datetime, till: datetime) -> None:
        """
        Renders bank statement for a period between since and till
        """
        # Table style
        table = PrettyTable(field_names=['Date', 'Description', 'Withdrawals', 'Deposits', 'Balance'],
                            min_width=15,
                            hrules=ALL)
        table.align['Date'] = 'l'
        table.align['Description'] = 'l'
        table.align['Withdrawals'] = 'r'
        table.align['Deposits'] = 'r'
        table.align['Balance'] = 'r'

        # First row
        row_balance = self.get_balance_by_date(since)
        table.add_row(['', 'Previous balance', '', '', p_format_money(row_balance)])

        # Main body (operations)
        operations_report = self.generate_operations_report(since, till, row_balance)
        table.add_rows(operations_report['rows'])

        # Last row
        table.add_row(['',
                       'Totals',
                       p_format_money(operations_report['withdrawals']),
                       p_format_money(operations_report['deposits']),
                       p_format_money(operations_report['total_balance']),
                       ])
        print(table)

    def generate_operations_report(self, since: datetime, till: datetime, row_balance: Money) -> dict:
        """
        Generates a dict-like report about operations in a period of time
        :param since: Start of time period
        :param till: End of time period
        :param row_balance: What balance was at the start of period
        :return: {'rows': list, 'withdrawals': Money, 'deposits': Money}
        """
        report = {
            "rows": [],
            "withdrawals": Money(0, self.currency),
            "deposits": Money(0, self.currency),
            "total_balance": Money(0, self.currency),
        }

        for operation in self.operations:
            if since <= operation.date <= till:
                row = operation.get_table_row()
                row_balance = self.change_balance(row_balance, operation)
                row.append(p_format_money(row_balance))
                report["rows"].append(row)
                report["total_balance"] = row_balance
                if operation.operation == "withdraw":
                    report["withdrawals"] += operation.amount
                if operation.operation == "deposit":
                    report["deposits"] += operation.amount

        return report

    @staticmethod
    def change_balance(balance: Money, operation: Operation) -> Money:
        """Adds or subtracts balance, depending on operation type"""
        if operation.operation == 'withdraw':
            return balance - operation.amount
        return balance + operation.amount

    def get_balance_by_date(self, date: datetime) -> Money:
        """
        Calculates account balance by iterating over operations. Assuming that list of operations is sorted by date
        :param date:  Date that will stop calculation
        :return: Balance (Money type)
        """
        balance = Money(0, currency=self.currency)
        for operation in self.operations:
            if operation.date <= date:
                balance = Account.change_balance(balance, operation)
            else:
                break
        return balance


if __name__ == '__main__':
    a = Account("Joe")
    b = Account("Joe")
    opers = []
    opers.append(Operation('deposit', '20', 'test deposit'))
    opers.append(Operation('deposit', '0.1', 'test deposit'))
    opers.append(Operation('deposit', '40', 'test deposit'))
    opers.append(Operation('withdraw', '30', 'test withdraw'))
    for o in opers:
        a.add_operation(o)
    since = datetime.strptime('2021-01-01 00:00:00', DATE_FORMAT)
    till = datetime.strptime('2021-05-01 00:00:00', DATE_FORMAT)
    a.show_bank_statement(since, till)
    assert a is b

#TODO START handler class
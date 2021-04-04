from functools import wraps
from datetime import datetime

import click
from click_shell import shell


from bank_app import Account
from bank_app.settings import DATE_FORMAT


def _clear_options(func):
    """
    This is a quick fix of leaking symbol `=` when using short command options, like `command -c="Joseph Jones"
    Removes symbol `=` from option stings
    Example: passed option `=Joseph Jones` -> turns into `Joseph Jones`
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        new_args = []
        new_kwargs = {}

        # clean args
        for arg in args:
            if isinstance(arg, str):
                if arg[0] == "=":
                    new_args.append(arg[1:])
                else:
                    new_args.append(arg)
            else:
                new_args.append(arg)

        # clean kwargs
        for key, val in kwargs.items():
            if isinstance(val, str):
                if val[0] == "=":
                    new_kwargs[key] = val[1:]
                else:
                    new_kwargs[key] = val
            else:
                new_kwargs[key] = val

        # run func with cleaned params
        func(*new_args, **new_kwargs)

    return wrapper


@shell(prompt=' > ', intro='Service started!')
def main():
    pass


@main.command()
@click.option('-c', '--client', 'client', required=True, type=str, prompt="Provide client name")
@click.option('-a', '--amount', 'amount', required=True, prompt="Amount")
@click.option('-d', '--description', 'description', required=False, type=str)
@_clear_options
def deposit(client, amount, description=None):
    """ Deposits money to account """
    try:
        account = Account(client)
        account.create_and_add_operation('deposit', amount, description)
        print('Deposit operation was successful!')
    except Exception as e:
        print(e)


@main.command()
@click.option('-c', '--client', 'client', required=True, type=str)
@click.option('-a', '--amount', 'amount', required=True)
@click.option('-d', '--description', 'description', required=False, type=str)
@_clear_options
def withdraw(client, amount, description=None):
    """ Withdraws money from account """
    try:
        account = Account(client)
        account.create_and_add_operation('withdraw', amount, description)
        print('Withdrawal operation was successful!')
    except Exception as e:
        print(e)


@main.command("show_bank_statement")
@click.option('-c', '--client', 'client', required=True, type=str)
@click.option('-s', '--since', 'since',
              required=True,
              type=click.DateTime(formats=[DATE_FORMAT, '=' + DATE_FORMAT]),
              help=f"Use format {DATE_FORMAT}",
              )
@click.option('-t', '--till', 'till',
              required=False,
              type=click.DateTime(formats=[DATE_FORMAT, '=' + DATE_FORMAT]),
              help=f"Use format {DATE_FORMAT}",
              )
@_clear_options
def show_bank_statement(client, since, till=datetime.now()):
    """ Renders client's bank statement with given time restrictions """
    till = till or datetime.now()
    account = Account(client)
    account.show_bank_statement(since, till)


if __name__ == '__main__':
    main()

# deposit -c="joe" -a=200 -d="ATM deposit"
# deposit -c="joe" -a=300 -d="ATM deposit"
# deposit -c="joe" -a=400 -d="ATM deposit"
# withdraw -c="joe" -a=1000 -d="ATM withdrawal"
# withdraw -c="joe" -a=-1000 -d="ATM withdrawal"
# withdraw -c="joe" -a=500.984 -d="ATM withdrawal"
# withdraw -c="joe" -a=100 -d="ATM withdrawal"
# show_bank_statement -c="joe" -s="2020-01-01 00:00:00" -t="2022-01-01 00:00:00"

from functools import partial

from moneyed.l10n import format_money

p_format_money = partial(format_money, locale='en_US')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CURRENCY = 'USD'

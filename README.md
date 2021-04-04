# NTpro task

To run:
* Clone repo and `cd` into it
* Create virtualenv (python 3.9.0 used in development)
* Install dependencies with `pip install -r requirements.txt`
* Run program with `python main.py`

Поддерживаемые приложением операции:  
* help - подскажет какие команды доступны
* exit / quit - для выхода из приложения
* deposit - операция пополнения счета на сумму, аргументы: client(-c / --client), amount (-a / --amount), description (-d / --description)
* withdraw - операция снятия со счета, аргументы: client (-c / --client), amount (-a / --amount), description (-d / --description)
* show_bank_statement - вывод на экран выписки со счета за период, аргументы:
client (-c / --client), since (-s / --since), till (-t / --till) 
  

Выполнение требований:
* работа с сервисом должна осуществляться через Interactive CLI
  * Done. Использовал библиотеки click + click-shell для настройки CLI
* состояние счетов хранится только в рамках одной сессии
  * Done. Все в оперативной памяти. Ничего не сохраняю на диск.
* у клиента может быть только один счет
  * Done. Реализовано через метакласс (перехват `__call__`)
* валюта у всех счетов одинаковая - USD
    * Done. Использовал библиотеку py-moneyed для работы с деньгами. Валюта зафиксирована в bank_app.settings.
* Поддерживаемые операции
    * Done. Описал выше. Также можно посмотреть их в CLI через `--help`
    
## Несколько операций для копипасты
* `deposit -c="joe" -a=200 -d="ATM deposit"`
* `deposit -c="joe" -a=300 -d="ATM deposit"`
* `deposit -c="joe" -a=400 -d="ATM deposit"`
* `withdraw -c="joe" -a=1000 -d="ATM withdrawal"`
* `withdraw -c="joe" -a=-1000 -d="ATM withdrawal"`
* `withdraw -c="joe" -a=500.984 -d="ATM withdrawal"`
* `withdraw -c="joe" -a=100 -d="ATM withdrawal"`
* `show_bank_statement -c="joe" -s="2020-01-01 00:00:00" -t="2022-01-01 00:00:00"`
* `show_bank_statement -c="joe" -s="2020-01-01 00:00:00"`
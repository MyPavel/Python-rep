# This Python file uses the following encoding: utf-8+
import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно переводить одинаковые валюты {base}. Введите /help для информации.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}. Введите /help для информации.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}. Введите /help для информации')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Введите /help для информации')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        resp = json.loads(r.content)[keys[base]]
        total_base = resp*amount
        total_base = round(total_base, 3)

        return total_base

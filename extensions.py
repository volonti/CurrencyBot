import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if type(quote) == str and type(base) == str:
            if quote == base:
                raise APIException(f"Невозможно конвертировать одинаковую валюту {quote}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}, введите цифры")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]
        sum = float(total_base) * float(amount)
        sum = round(sum, 2)

        return sum

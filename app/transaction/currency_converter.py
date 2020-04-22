import requests

api_key = "RXPVEK1KK0BD7B8S"


def currency_rate(from_currency, to_currency):
    """get exchange rate of 2 currencies"""
    url = str('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=' + from_currency +
              '&to_currency=' + to_currency + '&apikey=' + api_key)

    response = requests.get(url=url)
    result = response.json()

    return result["Realtime Currency Exchange Rate"]['5. Exchange Rate']


def payment_value(currency, amount, payment_currency):
    """get payment value after all taxes and charges"""
    conversion_charges_rate = 5.00     # in percent
    tax_rate = 10.00                   # in percent of conversion_charges

    converted_amount = amount*float(currency_rate(currency, payment_currency))
    conversion_charges = converted_amount*conversion_charges_rate/100
    tax = conversion_charges*tax_rate/100

    return converted_amount+conversion_charges+tax

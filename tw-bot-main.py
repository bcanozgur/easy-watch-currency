import requests
import time
import tweepy
import talib
import numpy as np


class XAUUSDBot:
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        self.url = "https://api.binance.com/api/v3/ticker/price?symbol=XAUUSDT"
        self.auth = tweepy.OAuthHandler(api_key, api_secret_key)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

    def get_price(self):
        response = requests.get(self.url)
        return float(response.json()['price'])

    def get_rsi(self, prices, timeperiod=14):
        prices = np.array(prices)
        rsi = talib.RSI(prices, timeperiod)
        return rsi[-1]

    def get_kama(self, prices, timeperiod=30):
        prices = np.array(prices)
        kama = talib.KAMA(prices, timeperiod)
        return kama[-1]

    def tweet(self, message):
        self.api.update_status(message)

    def run(self):
        while True:
            try:
                price = self.get_price()
                prices = [price]
                rsi = self.get_rsi(prices)
                kama = self.get_kama(prices)
                if rsi <= 30 and price <= kama:
                    message = f"XAUUSD: {price} - RSI: {rsi} - KAMA: {kama}"
                    self.tweet(message)
                    print("Tweet sent:", message)
                time.sleep(10)
            except Exception as e:
                print("An error occurred:", e)
                time.sleep(10)


if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    api_secret_key = "YOUR_API_SECRET_KEY"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

    bot = XAUUSDBot(api_key, api_secret_key, access_token, access_token_secret)
    bot.run()

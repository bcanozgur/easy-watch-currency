import requests
import talib
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sched
import time


class XAUUSDBot:
    def __init__(self, email, password, recipient_email):
        self.url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        self.email = email
        self.password = password
        self.recipient_email = recipient_email
        self.prices = []

    def get_price(self):
        response = requests.get(self.url)
        return float(response.json()['price'])

    def get_rsi(self):
        prices = np.array(self.prices)
        rsi = talib.RSI(prices, 14)
        return rsi[-1]

    def get_kama(self):
        prices = np.array(self.prices)
        kama = talib.KAMA(prices, 30)
        return kama[-1]

    def send_email(self, message):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.recipient_email
        msg['Subject'] = "XAUUSD Alert"
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        text = msg.as_string()
        server.sendmail(self.email, self.recipient_email, text)
        server.quit()
        print("Email sent:", message)

    def check_price(self):
        try:
            price = self.get_price()
            self.prices.append(price)
            rsi = self.get_rsi()
            kama = self.get_kama()
            if rsi <= 30 and price <= kama:
                message = f"XAUUSD: {price} - RSI: {rsi} - KAMA: {kama}"
                self.send_email(message)
            self.prices.pop(0)
        except Exception as e:
            print("An error occurred:", e)

    def run(self):
        s = sched.scheduler(time.time, time.sleep)
        while True:
            s.enter(10, 1, self.check_price, ())
            s.run()


if __name__ == "__main__":
    email = "YOUR_EMAIL_ADDRESS"
    password = "YOUR_EMAIL_PASSWORD"
    recipient_email = "RECIPIENT_EMAIL_ADDRESS"

    bot = XAUUSDBot(email, password, recipient_email)
    bot.run()

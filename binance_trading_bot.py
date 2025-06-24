
import logging
from binance.client import Client
from binance.enums import *
import time

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
        self.client = Client(api_key, api_secret)
        self.client.FUTURES_URL = self.base_url
        self.setup_logger()
        logging.info("Bot initialized with testnet: %s", testnet)

    def setup_logger(self):
        logging.basicConfig(filename="trading_bot.log", level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == "MARKET":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == "LIMIT":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                logging.error("Unsupported order type: %s", order_type)
                return None

            logging.info("Order placed: %s", order)
            print("Order placed successfully!")
            return order
        except Exception as e:
            logging.error("Error placing order: %s", str(e))
            print("Error:", str(e))
            return None

def get_user_input():
    print("=== Welcome to Binance Futures Testnet Bot ===")
    api_key = input("Enter your API Key: ").strip()
    api_secret = input("Enter your API Secret: ").strip()

    bot = BasicBot(api_key, api_secret)

    while True:
        symbol = input("Enter trading pair (e.g. BTCUSDT): ").upper()
        side = input("Buy or Sell? (BUY/SELL): ").upper()
        order_type = input("Order Type (MARKET/LIMIT): ").upper()
        quantity = float(input("Enter quantity: "))

        price = None
        if order_type == "LIMIT":
            price = input("Enter limit price: ")

        bot.place_order(symbol, side, order_type, quantity, price)

        cont = input("Place another order? (y/n): ").lower()
        if cont != 'y':
            print("Exiting...")
            break

if __name__ == "__main__":
    get_user_input()

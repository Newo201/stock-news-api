from news import News
import requests
from dotenv import load_dotenv
import os
load_dotenv()

STOCK_API_KEY = os.getenv('STOCK_API_KEY')
STOCK_INFO_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_INFO_FUNCTION = "TIME_SERIES_DAILY"
STOCK_INFO_DATA = 'Time Series (Daily)'
STOCK_CLOSE = '4. close'
DUMB_STOCK_ENDPOINT = "https://dumbstockapi.com/stock"

class Stocks(News):
    
    """
    Class for reading and extracting info for stocks
    
    Inherits attributes and methods from news
    
    Intermediate Functions (unlikely to call):
        info: extracts stock_data
        get_name: converts symbol into stock name
     
    Output Functions (likely to call)
        daily_return: calculates previous return for individual stock
        news: sends news for stocks
    """
    
    def __init__(self, stock_portfolio, price_change_threshold, cur_close_date):
        
        """
        Initialises asset class
        
        Inputs:
            stock_portfolio: a list of stocks -> list
            price_change_threshold: minimum price to send email for individual stocks as a percentage -> float  
        """
        
        super().__init__(price_change_threshold, cur_close_date) # Inherit attributes and methods from news class
        
        self.stock_portfolio = stock_portfolio
        
    def info(self, symbol):
        
        """
        Extracts the stock information from the stock API. 
        Returns the stock data in JSON format
        
        Args:
            symbol - the stock ticker -> str
        """

        # Parameters for stock API
        stock_params = {
            'function': STOCK_INFO_FUNCTION,
            'symbol': symbol,
            'apikey': STOCK_API_KEY
        }

        # Call stock API and get price data
        response = requests.get(STOCK_INFO_ENDPOINT, params = stock_params)
        stock_data = response.json()[STOCK_INFO_DATA]
        
        return stock_data
    
    def daily_return(self, stock_data):
    
        """
        Computes the last day's stock return on the stock data
        
        Args:
            stock_data: returned from the info function -> JSON
        """

        # Find previous 2 days
        stock_values = list(stock_data.values())
        prev_2_days = stock_values[:2]

        # Find closing price
        cur_close = float(prev_2_days[0][STOCK_CLOSE])
        prev_close = float(prev_2_days[1][STOCK_CLOSE])

        # Compute change in price                                  
        change = round(((cur_close - prev_close)/prev_close)*100, 2)

        return change
    
    def get_name(self, symbol, exchange):
        
        """
        Determines the full stock name from the ticker symbol for the purpose of searching news.

        Args:
            symbol: the stock ticker (e.g. AAPL) -> str
            exchange: the market listed, normally NASDAQ
        """

        params = {
            'exchanges': exchange,
            'ticker_search': symbol
        }

        response = requests.get(DUMB_STOCK_ENDPOINT, params = params)

        return response.json()[0]['name']
    
    def news(self):
        
        """
        Sends news for individual stocks based on stock portfolio

        Args:
            stock_portfolio: list of stocks -> list
        """

        for stock in self.stock_portfolio:

            data = self.info(stock)
            price_change = self.daily_return(data)
            stock_name = self.get_name(stock, 'NASDAQ')
            stock_news = self.get_news(stock_name, price_change)
            self.send_news(price_change, stock_news)
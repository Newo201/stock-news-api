from news import News
import requests
from dotenv import load_dotenv
import os
load_dotenv()

ALL_COINS_ENDPOINT = "https://api.coingecko.com/api/v3/coins"
COIN_API_KEY = os.getenv('COIN_API_KEY')
PRICE_DATA = 'market_data'
EXCHANGE = 'aud'

class Coins(News):
    
    """
    Class for information related to cryptocurrency
    
    Inherits attributes and methods from news
    
    Intermediate Functions (unlikely to call):
        api_call: makes a call to the coin API
        
    Output Functions (likely to call)
        get_all: returns all available coins
        is_valid_portfolio: determines if list provided is valid
        news: sends news for coins
    """
    
    def __init__(self, coin_portfolio, price_change_threshold, cur_close_date, coin_close_date, coin_prev_date):
        
        """
        Initialises Coins Class
        
        Inputs:
            price_change_threshold: to pass into News class
            coin_portfolio: list of valid coins
        
        Outputs:
            is_valid: checks if list provided is valid based on all coins
        """
        
        super().__init__(price_change_threshold, cur_close_date) # Inherit attributes and methods from news class
        self.coin_portfolio = coin_portfolio
        self.is_valid = self.is_valid_portfolio()
        self.coin_close_date = coin_close_date
        self.coin_prev_date = coin_prev_date
        
    def get_all(self):
        
        """
        Returns a list of all valid coins for the user to include
        """

        coins = requests.get(f'{ALL_COINS_ENDPOINT}/list', params = {'x_cg_demo_api_key': COIN_API_KEY}).json()
        all_coins = [coin['id'] for coin in coins]
        return all_coins
    
    def is_valid_portfolio(self):
        
        """
        Determines if the coin_list provided is valid, based on the coins listed in the coin API.

        Args:
            coin_portfolio: coins in the portfolio -> list
        """
        all_coins = self.get_all()
        for coin in self.coin_portfolio:
            if coin not in all_coins:
                raise Exception('You have not chosen valid coins, please look at all coins')    
        return True
    
    def api_call(self, date, single_coin):
        
        """
        Makes a call to the coin API and returns the closing price in AUD
        at a given date.


        Args:
            date - in dd-mm-yyyy format -> str
            coin - the coin we want to look at
        """

        # paramaters to parse into coin API
        coin_params = {
            'date': date,
            'localization': 'false',
            'x_cg_demo_api_key': COIN_API_KEY
        }

        # Get Response
        coin_endpoint = f'{ALL_COINS_ENDPOINT}/{single_coin}/history'
        response = requests.get(coin_endpoint, params = coin_params)

        # Find closing price in AUD
        coin_data = response.json()[PRICE_DATA]
        close = coin_data['current_price'][EXCHANGE]

        return close
    
    def daily_return(self):
        
        """
        Computes the return of each of the coins in the portfolio. Also checks if the portfolio is valid
        and prompts the user to change the portfolio otherwise.

        Args:
            coin_portfolio: coins in the portfolio -> list 
        """

        return_dict = dict()
        
        for coin in self.coin_portfolio:
      
            # Current close
            cur_close = self.api_call(self.coin_close_date, coin)

            # Previous day
            prev_close = self.api_call(self.coin_prev_date, coin)
            
            # daily_return
            daily_return = round(((cur_close - prev_close)/prev_close)*100, 2)
            return_dict[coin] = daily_return
            

        return return_dict   
    
    def news(self):
        
        """
        Sends news for individual coins
        """

        daily_return_dict = self.daily_return()

        for (coin, c_return) in daily_return_dict.items():
            coin_news = self.get_news(coin, c_return)
            self.send_news(c_return, coin_news)
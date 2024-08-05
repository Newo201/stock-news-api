import requests
import smtplib
from dotenv import load_dotenv
import os
load_dotenv()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
MY_EMAIL = os.getenv('EMAIL_ADDRESS')
MY_PASSWORD = os.getenv('EMAIL_PASSWORD')

class News():
    
    """
    This is the class for news related functions
    
    None of these functions will be called independently, because they are inherited by other classes.
    
    Functions:
        get_news: grabs the top three headlines
        send_news: sends headlines to email
    """
    
    def __init__(self, price_change_threshold, cur_close_date):
        
        """
        Initialises news class
        
        Inputs:
            price_change_threshold: minimnum price to send email for individual stocks as a percentage -> float
        """
        
        self.price_change_threshold = price_change_threshold
        self.cur_close_date = cur_close_date
        
        
    def get_news(self, stock_name, price_change):
        
        """
        Grabs the top three headlines based on search criteria and returns in an appropriate
        format to send emails

        Args:
            stock_name: the full name of the stock -> str
            price_change: the daily change in price -> float
        """

        # Declare parameters to pass in
        news_params = {
            'q': stock_name,
            'from': self.cur_close_date,
            'sortBy': 'popularity',
            'apiKey': NEWS_API_KEY
        }
        
        # Call response and get first three articles
        response = requests.get(NEWS_API_ENDPOINT, params = news_params)
        articles = response.json()['articles'][:3]

        # Find summaries for each article and combine
        summaries = []  
        for article in articles:
            headline = f"Headline: {article['title']}"
            brief = f"Brief: {article['description']}"
            summaries.append(f"{headline}\n{brief}\n\n")
        body = ''.join(summaries)

        # Add subject with price change
        if price_change < 0:        
            subject = f"Subject: {stock_name} ↓ {abs(price_change)}% over the past day"
        else:    
            subject = f"Subject: {stock_name} ↑ {price_change}% over the past day"

        return f"{subject}\n\n{body}"
        
    def send_news(self, price_change, message):    
        """
        Sends news to specified email if the price change is greater than some threshold.
        Currently sends separate emails for each asset.
        """

        if abs(price_change) > self.price_change_threshold:

            # Email setup
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)

            # Send message
            connection.sendmail(
                from_addr = MY_EMAIL,
                to_addrs = MY_EMAIL,
                msg = message.encode('utf-8')
            )
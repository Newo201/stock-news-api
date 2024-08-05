# Stock News API

The purpose of this program is to combine a few free APIs to deliver headlines about stocks and coins
in a portfolio. The news is only sent when the prices change more than a pre-specified amount. 

The usefulness of this project could be increased by using paid APIs to get access to better data, and running
the code on a platform which automatically executes the script every day (e.g. PythonAnywhere).

## How the Code Works

The News class finds all the headlines relating to an asset with a given provided name. We then extract the top 3 news sources,
separate them into headline and body and construct an email from the provided information. A possible extension on this
would be to populate this information into a website. 

The Stock class finds the closing price from the current and previous day and calculates a return. If the return exceeds some 
user defined threshold, then the news class is called to send an email. The coin class works in a similar way.

## Setup

### Email Setup

This class also uses the SMTP module to send an email with the news. There are a specific set of instructions which need to be followed to allow this to happen, which includes weakening the security of your email. I suggest setting up a new gmail account to do this. Please read [here](https://support.google.com/mail/answer/185833?hl=en) for more information on how to set up an app password.

### Stock News API

We use the News API to search news by topic. This requires the name of the company/crypto, as opposed to its symbol.

The endpoint used is "https://newsapi.org/v2/everything" where we can then search by name and sort by popularity.

### Stock Price API

Read [here](https://www.alphavantage.co/documentation/) for the full documentation. This requires an API key (no sign up necessary), and the free version only has access to limited endpoints.

We use the function called *Time_Series_Daily* since this is a free endpoint. There may be an opportunity to use *Time_Series_Intraday* in future versions of the code if there is a need to get return information on a regular basis.
 
Required Arguments

 - function: see above
 - symbol: e.g. IBM
 
The endpoint is the following: https://www.alphavantage.co/query

### Dumb Stock API

Matches stock ticker to stock name. Read [here](https://dumbstockapi.com/) for the full (but admittedly limited) documentation. Purpose of this section is to allow for an automated search of news in section 4, based off the ticker provided. This is only relevant for stocks, as the coins already include the name.

### Coin API

I wanted to use the CoinMarketCap API. [This Page](https://coinmarketcap.com/api/documentation/v1/#operation/getV2CryptocurrencyQuotesHistorical) seems particularly useful for the current project. Unfortunately, it is locked behind a paywall.

Instead I used [this free API](https://www.coingecko.com/en/api/documentation) called Coingecko which only requires an API key to use for a demo account.

Endpoints used are https://api.coingecko.com/api/v3/coins/list for seeing all the available coins and https://api.coingecko.com/api/v3/coins/{single_coin}/history for seeing the price of an individual coin.
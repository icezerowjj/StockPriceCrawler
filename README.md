# StockPriceCrawler

This Python project scrapes asset information from Investing.com by visiting the websites and crawling it down into SQL with time, 
ticker and prices as the columns.

Add the stock's website link to the Ticker.xlsx first for Python to read in. 

The WebLinkedList generates a linked list to store the webpage before working on beautifulsoup which can improve the efficiency a lot. 

The Utilities store the functions to support the main in CrawlInvesting.

User can change any information from the Investing.com web page from Inspect and the according position in beautifulsoup. 

Login has been tried so that user's portfolio can be displayed as a table. But it failed because Investing.com has some anti-robot 
program which avoids offering the token to log in. 

For those who want intraday stock price data but cannot afford the data supplier such as Interactive Broker, this program can generate 
your own database with the stock price data you want. 

# stock_market_plot_with_12Data_API

Welcome to the stock_market_plot_with_12Data_API wiki!

A python script using 12Data API to retrieve and plot stock market data.
The script plots the evolution of the share price and the dividends.
In the example I chose Apple (AAPL).

![image](https://user-images.githubusercontent.com/82118574/215887077-9fc17a09-d724-4cb2-a015-e8d8921267bb.png)

To make in works in your computer : 

* download the code using : 

`git clone https://github.com/MVALEX13/stock_market_plot_with_12Data_API.git`

* download the required python libraries :

`pip install -r requirements.txt`

* create an account on https://twelvedata.com/account. Once the account created you'll have an API_KEY.
 You'll need to replace `YOUR_API_KEY` in `MY_API_KEY='YOUR_API_KEY'` (line 19) with your own API.

* Then run the python program, Apple stock market data should be plotted.

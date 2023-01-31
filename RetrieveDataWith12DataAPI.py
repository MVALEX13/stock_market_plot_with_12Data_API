# ================================================================================================================================= #
# This script retreive time serie of stock market using 12Data API
# check the website : https://twelvedata.com/account
# ================================================================================================================================= #

### informations to acces with url request
# BASE_URL = 'https://api.twelvedata.com'
# ENDPOINT_SERIE = '/time_series'
# MY_API_KEY='a6a5b36967244bf286de09d7fa99cde8'

from twelvedata import TDClient                  # librairie for communicating easily with 12Data API
from datetime import date                       # ro read date in iso format
import matplotlib.pyplot as plt

### request parameters
# --- mandatory parameters
SYMBOL = 'AAPL'
INTERVAL = '1week'
MY_API_KEY='YOUR_API_KEY'

# --- optionnal parameters
START_DATE = '2010-01-01'
END_DATE = str( date.today() )                    # get the current date
OUTPUTSIZE = 5000                                 # maximum possible (the number of data will be conditionned by the selected dates)


### Get Stock Market Serie ###
# This function returns 2 lists : 
#       - the share price list (cours de l'action)
#       - the date list corresponding to the date associated with each share price
###
def GetStockMarketSerie():
    # Initialize client - apikey parameter is requiered
    td = TDClient(apikey = MY_API_KEY)

    # Construct the necessary time series and make the request
    ts = td.time_series(
        symbol= SYMBOL,
        interval= INTERVAL,
        start_date = START_DATE,
        end_date = END_DATE,
        outputsize = OUTPUTSIZE       
    )

    # reading the data from the API answer
    share_dict = dict()
    for week in ts.as_json():

        # average compuatation based on the stock share price at the beginning and at the end of each week
        average_share = ( float(week.get("open",0)) + float(week.get("close",0)) )/2 

        # we retreive the date of the beginning of the week
        date_cours = ( date.fromisoformat(week.get("datetime",0)) )

        # filling the dict
        share_dict[date_cours] = average_share
        

    counter = len(share_dict)
    print(f'number of data retreived : { counter }' )

    return share_dict



### Get Dividend List ###
# This function returns 2 lists : 
#       - the dividend list
#       - the date list corresponding to the date associated with each dividend element
###
def GetDividendDict():

    # Initialize client - apikey parameter is requiered
    td = TDClient(apikey = MY_API_KEY)
    
    dividends = td.get_dividends(
        symbol = SYMBOL,
        start_date = START_DATE,
        end_date = END_DATE
    ).as_json()['dividends']


    # reading the data from the API answer
    dividend_dict = dict()
    for elmt in dividends:
        # read data from the request answer
        dividend = ( float( elmt.get('amount',0) ) )
        date_dividend = ( date.fromisoformat(elmt.get('payment_date')))

        # filling the dict with data
        dividend_dict[date_dividend] = dividend

    counter = len(dividend_dict)
    print(f'number of data retreived : { counter }' )

    return dividend_dict







def PlotShareAndDividend(Share_dict, Dividend_dict):
    fig, ax = plt.subplots(2,1)
    fig.suptitle(SYMBOL)

    # plot share price 
    ax[0].set_title('Share price')
    ax[0].plot([key for (key,value) in Share_dict.items()], [value for (key,value) in Share_dict.items()],label = 'share')
    ax[0].set_ylabel('share price ($)')
    ax[0].legend()
    
    # plot dividends
    ax[1].set_title('Dividends')
    ax[1].stem([key for (key,value) in Dividend_dict.items()],[value for (key,value) in Dividend_dict.items()])
    ax[1].set_xlabel('time')
    ax[1].set_ylabel('dividends ($)')

    
    plt.show()



def main():

    share_dict = GetStockMarketSerie()

    dividend_dict = GetDividendDict()

    PlotShareAndDividend(share_dict, dividend_dict)



if __name__ == '__main__':
    main()




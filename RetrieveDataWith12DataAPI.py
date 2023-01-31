# ================================================================================================================================= #
# This script retreive time serie of stock market using 12Data API
# check the website : https://twelvedata.com/account
# ================================================================================================================================= #

### informations to acces with url request
# BASE_URL = 'https://api.twelvedata.com'
# ENDPOINT_SERIE = '/time_series'
# MY_API_KEY='a6a5b36967244bf286de09d7fa99cde8'

from twelvedata import TDClient                  # librairie for communicating easily with 12Data API
from datetime import date, datetime                       # ro read date in iso format
import matplotlib.pyplot as plt

### request parameters
# --- mandatory parameters
SYMBOL = 'AAPL'
INTERVAL = '1week'
MY_API_KEY='a6a5b36967244bf286de09d7fa99cde8'

# --- optionnal parameters
START_DATE = '2010-01-01'
END_DATE = str( date.today() )                    # get the current date
OUTPUTSIZE = 5000                                 # maximum possible (the number of data will be conditionned by the selected dates)


#####################################################################################################################################
# This function returns 2 lists : 
#       - the share price list (cours de l'action)
#       - the date list corresponding to the date associated with each share price
#####################################################################################################################################
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
    cours_dict = dict()
    for week in ts.as_json():

        # average compuatation based on the stock share price at the beginning and at the end of each week
        average_cours = ( float(week.get("open",0)) + float(week.get("close",0)) )/2 

        # we retreive the date of the beginning of the week
        date_cours = ( date.fromisoformat(week.get("datetime",0)) )

        # filling the dict
        cours_dict[date_cours] = average_cours
        

    counter = len(cours_dict)
    print(f'number of data retreived : { counter }' )

    return (cours_dict)



#####################################################################################################################################
# This function returns 2 lists : 
#       - the NBNPA (Benefice Net Per Action) or EPS (Earning Per Share) list
#       - the date list corresponding to the date associated with each BNPA element
#####################################################################################################################################
def GetBNPAList():

    # Initialize client - apikey parameter is requiered
    td = TDClient(apikey = MY_API_KEY)
    
    stat = td.get_earnings(
        symbol = SYMBOL,
        start_date = START_DATE,
        end_date = END_DATE
    ).as_json()

    # reading the data from the API answer
    BNPA_dict = dict()
    for elmt in stat:
        # read data from the request answer
        BNPA = ( float( elmt.get('eps_actual',0) ) )
        date_BNPA = ( date.fromisoformat(elmt.get('date')))

        # filling the dict with data
        BNPA_dict[date_BNPA] = BNPA

    counter = len(BNPA)
    print(f'number of data retreived : { counter }' )

    return (BNPA_dict)


#####################################################################################################################################
# This function returns 2 lists : 
#       - the dividend list
#       - the date list corresponding to the date associated with each dividend element
#####################################################################################################################################
def GetDividendList():

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

    return (dividend_dict)


#####################################################################################################################################
# This function modifies the sampling rate of (Share_date_list, Share_list) so that the sampling rate is the same of
# (BNPA_date_list, BNPA_list)'s. 
# (Share_date_list, Share_list) has a higher sample rate frequency that (BNPA_date_list, BNPA_list)
#####################################################################################################################################
# def Undersampling(Share_date_list, Share_list, BNPA_date_list, BNPA_list):
    # to complete



def PlotStockMarketSerie(date_list, cours_list):     
    fig, ax = plt.subplots()                      # fig is the window, ax is the plotting area
    ax.plot(date_list,cours_list)
    ax.set_xlabel('time')
    ax.set_ylabel('share price ($)')
    ax.set_title(SYMBOL)
    plt.show()

def PlotBNPA(date_list, cours_list):
    fig, ax = plt.subplots()                      # fig is the window, ax is the plotting area
    ax.plot(date_list,cours_list)
    ax.set_xlabel('time')
    ax.set_ylabel('BNPA ($)')
    ax.set_title(SYMBOL)
    plt.show()

def PlotShareAndDividend(Share_dict,Dividend_dict):
    fig, ax = plt.subplots(2,1)
    fig.suptitle(SYMBOL)

    ax[0].set_title('Share price')
    ax[0].plot([key for (key,value) in Share_dict.items()], [value for (key,value) in Share_dict.items()])
    ax[0].set_xlabel('time')
    ax[0].set_ylabel('share price ($)')
    
    ax[1].set_title('Dividend')
    ax[1].stem([key for (key,value) in Dividend_dict.items()],[value for (key,value) in Dividend_dict.items()])
    ax[1].set_xlabel('time')
    ax[1].set_ylabel('dividend ($)')
    

    plt.show()



def main():
    (Share_dict) = GetStockMarketSerie()
    (Dividend_dict) = GetDividendList()
    PlotShareAndDividend(Share_dict,Dividend_dict)


    


if __name__ == '__main__':
    main()




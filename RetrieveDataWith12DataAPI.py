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
MY_API_KEY='a6a5b36967244bf286de09d7fa99cde8'

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



### Get BNPA List ###
# This function returns 2 lists : 
#       - the NBNPA (Benefice Net Per Action) or EPS (Earning Per Share) list
#       - the date list corresponding to the date associated with each BNPA element
###
def GetBNPADict():

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

    counter = len(BNPA_dict)
    print(f'number of data retreived : { counter }' )

    return BNPA_dict


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

### Get Price Earning Ration Dict ###
# This function return a dictionnary that have the same key than
# share_dict_under_sampled and BNPA_dict.
# For each key the value will be the ratio of the
# share_dict_under_sampled value over the BNPA_dict value
###
def GetPriceEarningRatioDict(share_dict_under_sampled, BNPA_dict):
    PER_dict = dict()
    for key in share_dict_under_sampled:
        PER_dict[key] = share_dict_under_sampled.get(key)/BNPA_dict.get(key)
    
    return PER_dict 


### Get Share Dict Respecting PER ###
###
def GetShareDictRespectingPER(BNPA_dict, PER_value):
    share_dict = dict()
    for key in BNPA_dict:
        share_dict[key] = PER_value*BNPA_dict.get(key)
    
    return  share_dict

### Get Closest Index ###
# In our case the key of our dictionnaries are datetime.date
# So, for each of the dictionnary, the keys represent a set of datetime.date
# For a given datetime.date q_day this function returns the closest key among
# the set of datetime.dat
### 
def GetClosestIndex(share_dict, q_day):
    
    # the first key of the dict
    best_key = list(share_dict.keys())[0]
    
    # loop counter
    i = 0
    for key in share_dict:
        
        # check if the current key (which is a date) is closer that the date specified by the query q_day
        if ( abs((key-q_day).days) < abs((best_key-q_day).days) ):
            best_key = key
            
    return best_key







### Under Sample Dict ###
# In our case we have 2 dictionnaries share_dict and BNPA_dict. 
# Both of the dictionnaries have key of the type datetime.date.
# Later we'll want to make mathematical operation between the 2 dictionnaries.
# To make it possible, the 2 dictionnaries might have the same keys.
# This function returns a dictionnary that is, so to speak, a projection
# of the share_dict on the BNPA_dict. It means a dictionnary with the same key
# as the BNPA_dict but with values from share_dict.
###
def UnderSampleDict(dict_long, dict_short):
    
    # creation of new dict
    dict_long_SousEch = dict()
    
    for key in dict_short:
        
        # the key from dict_long that is the closest to 'key'
        closest_key = GetClosestIndex(dict_long,key)
        
        # filling the new dico with the estimated value for the key 'key'
        dict_long_SousEch[key] = dict_long[closest_key]
        
    return dict_long_SousEch






def PlotShareAndDividend(Share_dict, Share_dict_under_sampled, PER_dict, Share_dict_PER,PER_value, Dividend_dict):
    fig, ax = plt.subplots(2,2)
    fig.suptitle(SYMBOL)

    # plot share price 
    ax[0][0].set_title('Share price')
    ax[0][0].plot([key for (key,value) in Share_dict.items()], [value for (key,value) in Share_dict.items()],label = 'share')
    ax[0][0].plot([key for (key,value) in Share_dict_under_sampled.items()], [value for (key,value) in Share_dict_under_sampled.items()],label = 'share (under samled)')
    ax[0][0].plot([key for (key,value) in Share_dict_PER.items()], [value for (key,value) in Share_dict_PER.items()],label = ('share if PER = '+str(PER_value)) )
    ax[0][0].set_xlabel('time')
    ax[0][0].set_ylabel('share price ($)')
    ax[0][0].legend()
    
    # plot dividends
    ax[1][0].set_title('Dividends')
    ax[1][0].stem([key for (key,value) in Dividend_dict.items()],[value for (key,value) in Dividend_dict.items()])
    ax[1][0].set_xlabel('time')
    ax[1][0].set_ylabel('dividends ($)')

    # plot PE ratio
    ax[0][1].set_title('PE ration')
    ax[0][1].plot([key for (key,value) in PER_dict.items()], [value for (key,value) in PER_dict.items()],label = 'PER')
    ax[0][1].set_xlabel('time')
    ax[0][1].set_ylabel('PER($)')
    
    plt.show()



def main():
    BNPA_dict = GetBNPADict()

    share_dict = GetStockMarketSerie()

    share_dict_under_sampled = UnderSampleDict(share_dict,BNPA_dict)

    PER_dict = GetPriceEarningRatioDict(share_dict_under_sampled,BNPA_dict)

    PER_VALUE = 15
    share_dict_PER15 = GetShareDictRespectingPER(BNPA_dict,PER_VALUE)

    dividend_dict = GetDividendDict()
    PlotShareAndDividend(share_dict, share_dict_under_sampled, PER_dict, share_dict_PER15,PER_VALUE, dividend_dict)


    


if __name__ == '__main__':
    main()




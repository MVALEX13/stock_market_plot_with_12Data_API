# ================================================================================================================================= #
# This script retreive time serie of stock market using 12Data API
# check the website : https://twelvedata.com/account
# ================================================================================================================================= #

### informations to acces with url request
# BASE_URL = 'https://api.twelvedata.com'
# ENDPOINT_SERIE = '/time_series'
# MY_API_KEY='a6a5b36967244bf286de09d7fa99cde8'

from twelvedata import TDClient                  # librairie for communicating easily with 12Data API
from datetime import date                        # ro read date in iso format
import matplotlib.pyplot as plt

### request parameters
# --- mandatory parameters
SYMBOL = 'AAPL'
INTERVAL = '1week'
MY_API_KEY='a6a5b36967244bf286de09d7fa99cde8'

# --- optionnal parameters
START_DATE = '2010-01-01'
END_DATE = '2023-01-30'
OUTPUTSIZE = 5000                                 # maximum possible (the number of data will be conditionned by the selected dates)



### This function ask the API to send a specific time serie. Then the function returns a list with share prices and a list with dates
def GetStockMarketSerie():
    # Initialize client - apikey parameter is requiered
    td = TDClient(apikey = MY_API_KEY)

    # Construct the necessary time series
    ts = td.time_series(
        symbol= SYMBOL,
        interval= INTERVAL,
        start_date = START_DATE,
        end_date = END_DATE,
        outputsize = OUTPUTSIZE       
    )

    cours_list = list()
    date_list = list()
    for week in ts.as_json():

        # average compuatation based on the stock share price at the beginning and at the end of each week
        average_cours = ( float(week.get("open",0)) + float(week.get("close",0)) )/2 
        cours_list.append(average_cours)

        # we retreive the date of the beginning of the week
        date_list.append ( date.fromisoformat(week.get("datetime",0)) )
        

    counter = len(cours_list)
    print(f'number of data retreived : { counter }' )

    return (date_list,cours_list)





def PlotStockMarketSerie(date_list, cours_list):     
    fig, ax = plt.subplots()                      # figure creation
    ax.plot(date_list,cours_list)
    plt.show()



def main():
    (date_list, cours_list) = GetStockMarketSerie()
    
    PlotStockMarketSerie(date_list, cours_list)
    


if __name__ == '__main__':
    main()




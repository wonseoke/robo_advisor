# app/robo_advisor.py

import csv
import json
import os
from dotenv import load_dotenv
from datetime import datetime

import requests

load_dotenv() #> loads contents of the .env file into the script's environment

def to_usd(my_price):
     return f"${my_price:,.2f}" #> $12,000.71
#
# INFO INPUTS
#
api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 

symbol = input("Please input the stock symbol in question: ") #to accept USER INPUT


#
#SYMBOL LOOK UP to NASDAQ LIST
#
csv_file_path2 = os.path.join(os.path.dirname(__file__), "..", "data", "listed.csv") #to call a listed securities information from NASDAQ (http://nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt)

listed_stocks_info = [] #list of all information
with open(csv_file_path2, "r") as csv_file2:
    reader = csv.DictReader(csv_file2)
    for od in reader:
        listed_stocks_info.append(dict(od))

list_sec = [str(i["Symbol"]) for i in listed_stocks_info] #list of NASDAQ listed symbols

if symbol in list_sec:
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"        
else:
    print("Not a valid symbol, therefore we are exiting the query") & exit()


#
#SYMBOL LOOK UP to NASDAQ LIST
#

response = requests.get(request_url)
#print(type(response)) #> <class 'requests.models.Response'>
#print(response.status_code) #>200, which is the code of http response that lets us know how successful this request was
#print(response.text) #> #actual body of the response

parsed_response = json.loads(response.text)  #> makes the json/requested url to a readable dictionary.

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

#breakpoint()

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())  # TODO: assumes first day is on top, but consider sorting to ensure latest day is first

latest_day = dates[0] #"2020-06-12"
latest_close = tsd[latest_day]["4. close"] #> 1000000



# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%H:%M %p" + " on " + "%Y-%m-%d")

#get high price from each day
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))


recent_high = max(high_prices)
recent_low = min(low_prices)

#csv_file_path = "data/prices.csv" # a relative filepath

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date, 
            "open": daily_prices["1. open"], 
            "high": daily_prices["2. high"],  
            "low": daily_prices["3. low"], 
            "close": daily_prices["4. close"],  
            "volume": daily_prices["5. volume"],  
        })


#
#NASDAQ Prices look up
#
request_url_NDAQ = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=NDAQ&apikey={api_key}"
response_NDAQ = requests.get(request_url_NDAQ)
parsed_response_NDAQ = json.loads(response_NDAQ.text)
tsd_NDAQ = parsed_response_NDAQ["Time Series (Daily)"]

latest_close_NDAQ = tsd_NDAQ[latest_day]["4. close"]
high_prices_NDAQ = []
low_prices_NDAQ = []

for date in dates:
    high_price_NDAQ = tsd_NDAQ[date]["2. high"]
    high_prices_NDAQ.append(float(high_price_NDAQ))
    low_price_NDAQ = tsd_NDAQ[date]["3. low"]
    low_prices_NDAQ.append(float(low_price_NDAQ))

recent_high_NDAQ = max(high_prices_NDAQ)
recent_low_NDAQ = min(low_prices_NDAQ)
#print("NDAQ Latest: ", to_usd(float(latest_close_NDAQ)))
#print("NDAQ High: ", to_usd(float(recent_high_NDAQ)))
#print("NDAQ Low: ", to_usd(float(recent_low_NDAQ)))
#
#
#

#Recommendation logic is comparing the Nasdaq(market) performance vs. Inputted stock's performance
#This is done by comparing the Latest Price vs. average price (calculated by (recent high + recent low)/2 ))
#If a stock's latest_price/average_price is higher than Nasdaq's latest_price/average_price, it could mean it is further away from market's performance
#This could be a signal that the stock is overpriced versus the market; Then the recommendation should be SELL.
#Vice versa, if the stock's latest_price/average_price is lower, then the recommendation should be BUY.
#For NDAQ look up, the recommendation should be HOLD as the calculated value will be the same.

recommend = 0
reason = 0
average_price = (float(recent_high) + float(recent_low)) / 2
average_price_NDAQ = (float(recent_high_NDAQ) + float(recent_low_NDAQ)) / 2
calc_stock = float(latest_close) / float(average_price) 
calc_NDAQ = float(latest_close_NDAQ) / float(average_price_NDAQ)


if float(calc_stock) > float(calc_NDAQ):
    recommend = "SELL"
    reason = "We are recommending to sell the queried stock as the stock is considered over-priced compared to the overall market"
elif float(calc_stock) == float(calc_NDAQ):
    recommend = "HOLD"
    reason = "We are recommending to hold the queried stock as NDAQ is simply tracking the market overall"
else:
    recommend = "BUY"
    reason = "We are recommending to buy the queried stock as the stock is considered under-priced compared to the overall market"

print("-------------------------")
print("SELECTED SYMBOL: " + symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("Run at: ", dt_string)  ## TODO : get date time module
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {recommend}")
print(f"RECOMMENDATION REASON: {reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path} ")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")





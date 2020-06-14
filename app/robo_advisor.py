# app/robo_advisor.py

import csv
import json
import os
from dotenv import load_dotenv

import requests

load_dotenv() #> loads contents of the .env file into the script's environment

def to_usd(my_price):
     return f"${my_price:,.2f}" #> $12,000.71
#
# INFO INPUTS
#
api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 

symbol = "IBM" #TODO to accept USER INPUT

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

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


#get high price from each day

#high_price = [10, 20, 30]
# maximum of all high prices
#recent_high = max(high_price)


high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))


recent_high = max(high_prices)
recent_low = min(low_prices)
#
#
#
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



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")  ## TODO : get date time module
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path} ")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")





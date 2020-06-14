# app/robo_advisor.py

import requests
import json

def to_usd(my_price):
     return f"${my_price:,.2f}" #> $12,000.71
#
# INFO INPUTS
#
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"

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

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))

recent_high = max(high_prices)
#
#
#



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")  ## TODO : get date time module
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
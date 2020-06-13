# app/robo_advisor.py

import requests
import json


#
# INFO INPUTS
#
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"

response = requests.get(request_url)
#print(type(response)) #> <class 'requests.models.Response'>
#print(response.status_code) #>200, which is the code of http response that lets us know how successful this request was
#print(response.text) #> #actual body of the response

parsed_response = json.loads(response.text)  #> makes the json/requested url to a readable dictionary.

print(type(parsed_response))


breakpoint()



#
#
#



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
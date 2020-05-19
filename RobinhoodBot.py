from pyrh import Robinhood
import numpy as np
import tulipy as ti
import sched
import time
#A Simple Robinhood Python Trading Bot using RSI (buy <=30 and sell >=70 RSI)
#Youtube : Jacob Amaral
# Log in to Robinhood app (will prompt for two-factor)
rh = Robinhood()
rh.login(username="Robinhood Username Here", password="Robinhood Password")
#Setup our variables, we haven't entered a trade yet and our RSI period
enteredTrade = False
rsiPeriod = 5
#Initiate our scheduler so we can keep checking every minute for new price changes
s = sched.scheduler(time.time, time.sleep)
def run(sc): 
    global enteredTrade
    global rsiPeriod
    print("Getting historical quotes")
    # Get 5 minute bar data for Ford stock
    historical_quotes = rh.get_historical_quotes("F", "5minute", "day")
    closePrices = []
    #format close prices for RSI
    currentIndex = 0
    for key in historical_quotes["results"][0]["historicals"]:
        if (currentIndex >= len(historical_quotes["results"][0]["historicals"]) - (rsiPeriod + 1)):
            closePrices.append(float(key['close_price']))
        currentIndex += 1
    DATA = np.array(closePrices)
    print(len(closePrices))
    if (len(closePrices) > (rsiPeriod)):
        #Calculate RSI
        rsi = ti.rsi(DATA, period=rsiPeriod)
        instrument = rh.instruments("F")[0]
        #If rsi is less than or equal to 30 buy
        if rsi[len(rsi) - 1] <= 30 and not enteredTrade:
            print("Buying RSI is below 30!")
            rh.place_buy_order(instrument, 1)
            enteredTrade = True
        #Sell when RSI reaches 70
        if rsi[len(rsi) - 1] >= 70 and enteredTrade:
            print("Selling RSI is above 70!")
            rh.place_sell_order(instrument, 1)
            enteredTrade = False
        print(rsi)
    #call this method again every 5 minutes for new price changes
    s.enter(300, 1, run, (sc,))

s.enter(1, 1, run, (s,))
s.run()

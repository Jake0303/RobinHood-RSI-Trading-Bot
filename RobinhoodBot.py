from pyrh import Robinhood
import numpy as np
import tulipy as ti
import sched, time
# Log in to app (will prompt for two-factor)
rh = Robinhood()
rh.login(username="RobinHood Login Email Here", password="Robinhood Password Here")
enteredTrade = False
s = sched.scheduler(time.time, time.sleep)
def run(sc): 
    global enteredTrade
    print("Getting historical quotes")
    # do your stuff
    historical_quotes = rh.get_historical_quotes("F", "5minute", "day")
    closePrices = [];
    #format close prices for RSI
    for key in historical_quotes["results"][0]["historicals"]:
        closePrices.append(float(key['close_price']))
    DATA = np.array(closePrices)
    #Calculate RSI
    rsi = ti.rsi(DATA, period=5)
    instrument = rh.instruments("F")[0]
    #If rsi is less than or equal to 30 buy
    if rsi[len(rsi)-1] <= 30 and not enteredTrade:
        enteredTrade = True
        rh.place_buy_order(instrument, 1)
    #Sell when RSI reaches 70
    if rsi[len(rsi)-1] >= 70 and enteredTrade:
        rh.place_sell_order(instrument, 1)
        enteredTrade = False
    print(rsi[len(rsi)-1])
    s.enter(60, 1, run, (sc,))

s.enter(60, 1, run, (s,))
s.run()
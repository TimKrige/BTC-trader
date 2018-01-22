# This code accepts a CSV with the data in the format accessible from bfxdata.com
# CSV data must have early trade first, and the code assumes that the data is per unit time.
# If actual websocket data was used, the data must be made time-based by sampling the latest data with a thread tick
# If data is not time dependent, the momentum will be influenced by high frequency trades

import csv

portfolio = [100, 0] #[USD,BTC]
ema = 0              #Position
delta_ema = 0        #Velocity
momentum = 0
price = 0
vol = 0
buyandholdbtc = 0

def ema_update(latest_price):
    global ema, delta_ema
    if ema == 0:
        ema = latest_price
    else:
        ema_new = ema * 0.75 + 0.25 * latest_price
        delta_ema = (ema_new - ema)
        ema = ema_new
        
def buy(cost, amount):
    # Would code API access in here to place buy order
    global portfolio
    portfolio[1] = amount / cost
    portfolio[0] -= amount
    
def sell(cost, amount):
    # Would code API access in her to place sell order
    global portfolio
    portfolio[0] = amount * cost
    portfolio[1] -= amount
    
with open('data.csv', newline='') as datafile:
    datareader = csv.reader(datafile, delimiter=',') 
    next(datareader, None)
    for i in datareader:
        
        # initial buy, for buy and hold
        if price == 0:
            buyandhold = 100 / float(i[2])
        
        # updating prices and volumes
        price = float(i[2])
        vol = float(i[3])
        ema_update(price)
        
        momentum = vol * delta_ema
        
        # Trader logic here, using basic logic of momentum
        if momentum > 0:
            if portfolio[0] > 0:
                buy(price, portfolio[0])
                print("Placing buy order at :", i[1])
        elif momentum < 0:
            if portfolio[1] > 0:
                sell(price, portfolio[1])
                print("Placing sell order at :", i[1])


print('*********************************************************************************\nDone\n')
print('Final Account :', round((portfolio[0] + portfolio[1] * price), 2), 'USD')
print('Buy and hold :', round((buyandhold * price), 2))
print('Percentage Improvement :', round((((portfolio[0] + portfolio[1] * price)/(buyandhold * price) - 1) * 100), 2), '%')

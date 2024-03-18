import matplotlib.pyplot as plt

def calculate_ema(N, data):
  alpha = 2 / (N + 1)
  ema = [data[0]]
  for i in range(1, len(data)):
    ema_value = alpha * data[i] + (1 - alpha) * ema[-1]
    ema.append(ema_value)
  return ema

def buy(balance, price):
   return balance / price, 0

def sell(shares, price):
   return shares * price, 0

def calculate_profit(macd_transaction_history, sell_price):
   return sell_price - macd_transaction_history[-1]

with open('aapl_us_d.csv', 'r') as file:
  lines = file.readlines()

dates = []
prices = []
for line in lines:
    date_price = line.split(',')
    dates.append(date_price[0]) 
    prices.append(float(date_price[4]))

ema_12 = calculate_ema(12, prices)
ema_26 = calculate_ema(26, prices)

macd = [x - y for x, y in zip(ema_12, ema_26)]
signal = calculate_ema(9, macd)

balance = 0
shares = 1000
balance_before = sell(shares, prices[0])[0]

#apple stock price chart
plt.figure(figsize=(10, 6))
plt.plot(prices, label='Prices', color='blue')
plt.legend()
plt.title('Apple stock price')
plt.xlabel('Days')
plt.ylabel('Price')
plt.grid(True)
plt.show()

macd_transaction_history = []
macd_transaction_history.append(0)
macd_buying_history = []
macd_buying_history.append(0)

cash_balance_history = []
shares_without_selling = 1000
cash_balance_without_selling = []

#MACD and SIGNAL chart with buy/sell points
plt.figure(figsize=(10, 6))
plt.plot(macd, label='MACD', color='blue')
plt.plot(signal, label='Signal Line', color='orange')
was_buy_addes = False
was_sell_added = False
for i in range(0, len(macd)):
    if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:
        if was_buy_addes == False:
           plt.scatter(i, macd[i], color='green', marker='^', label="Buy")
           was_buy_addes = True
        else:
           plt.scatter(i, macd[i], color='green', marker='^')
        if balance > 0:
          macd_buying_history.append(balance)
          shares, balance = buy(balance, prices[i])
    elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
        if was_sell_added == False:
            plt.scatter(i, macd[i], color='red', marker='v', label="Sell")
            was_sell_added = True
        else:
           plt.scatter(i, macd[i], color='red', marker='v')
        if shares > 0:
          balance, shares = sell(shares, prices[i])
          macd_transaction_history.append(calculate_profit(macd_buying_history, balance)) #balance after selling - balance before buying
    if shares > 0:
       cash_balance_history.append(sell(shares, prices[i])[0])
    else:
       cash_balance_history.append(balance)
    cash_balance_without_selling.append(sell(shares_without_selling, prices[i])[0])
          
       
balance, shares = sell(shares, prices[-1])  #end of an investment
total_profit = balance - balance_before
balance_without_selling = sell(shares_without_selling, prices[-1])[0]

plt.legend()
plt.title('MACD and Signal Line')
plt.xlabel('Days')
plt.ylabel('Value')
plt.grid(True)
plt.show()

#MACD Transaction Profit/Loss Analysis
plt.figure(figsize=(10, 6))
plt.bar(range(len(macd_transaction_history)), macd_transaction_history, label='MACD Ratio', color='blue')
plt.legend()
plt.title('MACD balance')
plt.xlabel('Transaction number')
plt.ylabel('Profit')
plt.grid(True)
plt.show()

#Asset Valuation with MACD Strategy
plt.figure(figsize=(10, 6))
plt.plot(cash_balance_history, label='Money balance', color='blue')
plt.legend()
plt.title('Cash balance history')
plt.xlabel('Days')
plt.ylabel('Amount of money')
plt.grid(True)
plt.show()

#passive holding vs MACD
plt.figure(figsize=(10, 6))
plt.plot(cash_balance_history, label='Money balance using MACD', color='blue')
plt.plot(cash_balance_without_selling, label='Money balance using passive holding', color='red')
plt.legend()
plt.title('Comparison of Investment Strategies: MACD vs Passive Holding')
plt.xlabel('Days')
plt.ylabel('Amount of money')
plt.grid(True)
plt.show()
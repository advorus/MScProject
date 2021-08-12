"""Run this file."""

from traders import MarketMaker, RetailTrader
from exchange import Exchange
from order import Order
from globals import ASSET_CODE
import matplotlib.pyplot as plt
import random


ASSETS = [ASSET_CODE,'AAPL']
TEST_EX = Exchange(ASSETS)

testOrder = Order('001',10,ASSET_CODE,1,0,9.5,'firstbuy')
testOrder1 = Order('002',20,ASSET_CODE,1,1,12.5,'firstsell')

maker1 = MarketMaker('maker', TEST_EX, 2000)
makers = [MarketMaker('maker'+str(i), TEST_EX, 2000) for i in range(10)]
retail = [RetailTrader('retail'+str(i),TEST_EX, 2000) for i in range(10)]
#place test orders
TEST_EX.place_order(testOrder, 0)
TEST_EX.place_order(testOrder1, 0)

best_asks = []
best_bids = []
traders = makers+retail

for i in range(2000):
    TEST_EX.matched_orders_dict[i] = []
    
    random.shuffle(traders)
    for trader in traders:
        if i<200:
            if trader.type == "market_maker":
                trader.run(0.25,0.5,i)
            elif trader.type == "retail":
                pass
            else:
                raise Exception("unknown trader type")
        else:
            trader.run(0.25,0.5,i)

    best_asks.append(TEST_EX.get_best_ask(ASSET_CODE))
    best_bids.append(TEST_EX.get_best_bid(ASSET_CODE))

    TEST_EX.revise_account_values(i)

plt.plot(best_asks, label ="asks")
plt.plot(best_bids, label="bids")
plt.title("Best Bid/Ask in the Simulated Marketplace")
plt.legend()
plt.show()


# TEST_EX.showOrders('BTC')

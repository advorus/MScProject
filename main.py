"""Run this file."""

from exchange import Exchange
from order import Order

ASSETS = ['BTC','AAPL']
TEST_EX = Exchange(ASSETS)

testOrder = Order('001',10,'BTC',1,0,10,'tester')
testOrder1 = Order('002',20,'BTC',1,1,9.0,'tester1')

TEST_EX.place_order(testOrder)
TEST_EX.place_order(testOrder1)

# TEST_EX.showOrders('BTC')
TEST_EX.revise_account_values(0)
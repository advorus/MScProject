"""Holds the exchange class."""

from matchedOrders import MatchedOrders
from orderbook import Orderbook
from globals import *

class Exchange():
    """Will hold the simulation."""

    def __init__(self, assets):
        """
        Create an orderbook.

        :param assets: list of asset codes
        """
        self.assets = assets

        # establish a dictionary of orderbooks - one for each asset in the
        # exchange
        self.orderbooks = {}
        for asset in assets:
            self.orderbooks[asset] = Orderbook(asset)

        # orders will go into here after they get matched - contains a
        # dictionary of lists, each time step getting its own list of 
        # orders that have been matched that timestep
        self.matched_orders_dict = {0: []}
        
        #agents who get an order matched will be added to this list
        self.agents_with_matched_orders = []

        self.accountValues = {}

    def place_order(self,order):
        maxOrderCost = order.price
        trader = order.trader_code
        # if the trader doesn't have an account value then give him one
        if trader not in self.accountValues:
            self.accountValues[trader] = STARTING_ACCOUNT_VALUE
            
            print("Trader %s is trying to place an order but has no account value, so giving them the default account value of %d" % (order.trader_code, STARTING_ACCOUNT_VALUE))
            
            self.orderbooks[order.asset_code].place_order(order, self.matched_orders_dict[0])
        
        # if the trader doesn't have enough margin posted in his account then
        # don't allow him to place the order
        elif self.accountValues[trader] < order.price:
            raise Exception('Trader %s does not have the required funds to place order %s' % (order.trader_code,order.code))
        
        else:
            self.orderbooks[order.asset_code].place_order(order, self.matched_orders_dict[0])

    def run_simulation(self):
        print("testing")

    # revise the account values of all traders here
    def revise_account_values(self, tick):
        net_position_changes = {}

        for trader in self.accountValues:
            net_position_changes[trader] = 0

        for matched_order in self.matched_orders_dict[tick]:
            net_position_changes[matched_order.buyer_code] -= matched_order.execution_price * matched_order.volume
            net_position_changes[matched_order.seller_code] += matched_order.execution_price * matched_order.volume
            
        for trader in self.accountValues:
            self.accountValues[trader] += net_position_changes[trader]
    
            print('Trader %s has had their account value changed to %d' % (trader, self.accountValues[trader]))
    
    def showOrders(self, asset_code):
        self.orderbooks[asset_code].printBuffer()

    accountValues = {}

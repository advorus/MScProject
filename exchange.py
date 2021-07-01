"""Holds the exchange class."""

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
        self.matched_orders_dict = {}
        
        #agents who get an order matched will be added to this list
        self.agents_with_matched_orders = []

    def place_order(self,order):
        maxOrderCost = order.price
        # if the trader doesn't have an account value then give him one
        if not self.accountValues.trader:
            self.__accountValues.trader = STARTING_ACCOUNT_VALUE
        # if the trader doesn't have enough margin posted in his account then
        # don't allow him to place the order
        elif self.__accountValues.trader < order.price:
            raise Exception('Trader %f does not have the required funds to place order %f' % (order.trader_code,order.code))
        else:
            self.orderbooks[order.asset_code].place_order(order)

    def run_simulation(self):
        print("testing")

    __accountValues = {}

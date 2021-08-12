"""Contains Orderbook class."""

from LIBRAmatcher import LIBRA_Buffer, LIBRAmatcher
from FCFSmatcher import FCFSmatcher
from order import Order
from matchedOrders import MatchedOrders
from globals import *

class Orderbook():
    """Will hold and store orders - might also contain the matching logic."""

    def __init__(self, name, mechanism_name = MATCHING_PROTOCOL):
        """Initialize the Orderbook."""
        self.name = name
        self.buffer_length = 1

        self.orderList = {0: [Order('placeholder1',1e10,self.name,1,0,0,'exchange')], 1e10: [Order('placeholder2',1e10,self.name,1,0,1e10, 'exchange')]}

        self.best_bid=0
        self.best_offer = 1e10

        self.entry_buffer = []
        
        self.askPrices = set([1e10])
        self.bidPrices = set([0])

        if mechanism_name == 'FCFS':
            self.matcher = FCFSmatcher(self.buffer_length)
        elif mechanism_name == 'LIBRA':
            self.matcher = LIBRAmatcher()

    # method that traders will use to place an order
    def call_book(self, order_history, order = None):
        self.matcher.update_bests(self.best_bid, self.best_offer)
        
        if order:
            self.matcher.enter_order(order)
        
        orders_to_push = self.matcher.pull_down_orders()
        
        for order in orders_to_push:
            self.empty_order_from_buffer(order, order_history)
        orders_to_push = []

    # used to push an order straight into the book e.g. during the initiation of the book
    def place_order(self, order, order_history):
        """Adds an order to the entry buffer, that will then be processed by the exchange"""
        print('Manually firing an order into the orderbook')
        self.empty_order_from_buffer(order, order_history)
        
    
    # DEPRECATED METHOD
    # def old_place_order(self, order, order_history):
    #     """Adds an order to the entry buffer, that will then be processed by the exchange"""
    #     self.entry_buffer.append(order)
    #     print("Adding an order from %s to the buffer"% order.trader_code)

    #     len(self.entry_buffer)
    #     if(len(self.entry_buffer)==self.buffer_length):
    #         if MATCHING_PROTOCOL == 'FCFS':
    #             print('Emptying buffer as it contains %d orders'%len(self.entry_buffer))
    #             for order in self.entry_buffer:
    #                 self.empty_order_from_buffer(order, order_history)
    #             self.entry_buffer = []
    #         else:
    #             raise Exception('matching protocol has not been recognised')

    def empty_order_from_buffer(self, order, order_history):
        #this is where the matching logic comes in
        #for each order in the buffer perform the matching protocol
        # for order in self.entry_buffer:
        
        # if the order is a buy order then check against existing ask prices
        if(order.dir == 0):
            # cycle until the order has been extinguished, either by
            # matching or by placing it into the book
            
            while order.price >= self.best_offer:
                
                best_offer_list = self.orderList[self.best_offer]

                while len(best_offer_list) > 0:
                    sell_order = best_offer_list[0]
                    if sell_order.volume <= order.volume:
                        # TODO: change the account values in the exchange? Potentially do it
                        # at the end of each simulation tick - this resembles clearing house
                        # behaviour in the real world

                        # append the match that just happened to the order history
                        order_history.append(MatchedOrders(order.trader_code,sell_order.trader_code,sell_order.price,sell_order.volume,order.code,sell_order.code))
                        
                        order.volume-=sell_order.volume
                        best_offer_list.pop(0)
                        print("Matched %d units between buy order %s and sell order %s, execution price %f" % (sell_order.volume,order.code,sell_order.code,sell_order.price))
                    
                    else:
                        if sell_order.volume > order.volume:
                            sell_order.volume -= order.volume
                            order.volume = 0
                        else:
                            best_offer_list.pop(0)
                            order.volume = 0

                        order_history.append(MatchedOrders(order.trader_code,sell_order.trader_code,sell_order.price,order.volume,order.code,sell_order.code))
                        print("Matched %d units between buy order %s and sell order %s, execution price %f" % (order.volume,order.code,sell_order.code,sell_order.price))
                        return 0

                # only do this when the above is not true        
                # there are no longer any orders at the given price level        
                self.askPrices.remove(self.best_offer)
                # find the new best offer price
                self.best_offer = min(self.askPrices)
            
            #if the code gets to here then place an order in the orderbook with the characteristics of order
            # to get around the possibility that there is no defined list for the given price
            if order.volume > 0:
                try:
                    self.orderList[order.price]
                except KeyError:
                    self.orderList[order.price] = [order]
                else:
                    self.orderList[order.price].append(order)


                self.bidPrices.add(order.price)
                # print(self.bidPrices)
                self.best_bid = max(self.bidPrices)

                print("Placed new buy order in the book - %d units at %f from %s"%(order.volume, order.price,order.trader_code))
                return 0

        # if the order is a sell order then check against existing bid prices
        elif order.dir == 1:
            
            while order.price <= self.best_bid:
                # print(self.best_bid)
                best_offer_list = self.orderList[self.best_bid]

                while len(best_offer_list) > 0:
                    buy_order = best_offer_list[0]
                    if buy_order.volume <= order.volume:
                        # TODO: change the account values in the exchange? Potentially do it
                        # at the end of each simulation tick - this resembles clearing house
                        # behaviour in the real world

                        # append the match that just happened to the order history
                        order_history.append(MatchedOrders(buy_order.trader_code,order.trader_code,buy_order.price,buy_order.volume,buy_order.code,order.code))
                        
                        order.volume -= buy_order.volume
                        best_offer_list.pop(0)
                        print("Matched %d units between buy order %s and sell order %s, execution price %f" % (buy_order.volume,buy_order.code,order.code,buy_order.price))
                    
                    else:
                        if buy_order.volume > order.volume:
                            buy_order.volume -= order.volume
                            order.volume = 0
                        else:
                            best_offer_list.pop(0)
                            order.volume = 0
                            print('testing')

                        order_history.append(MatchedOrders(buy_order.trader_code,order.trader_code,buy_order.price,order.volume,buy_order.code,order.code))
                        print("Matched %d units between buy order %s and sell order %s, execution price %f" % (order.volume,buy_order.code,order.code,buy_order.price))
                        return 0

                # only do this when the above is not true        
                # there are no longer any orders at the given price level        
                self.bidPrices.remove(self.best_bid)
                # find the new best offer price
                self.best_bid = max(self.bidPrices)
            
            #if the code gets to here then place an order in the orderbook with the characteristics of order
            if(order.volume > 0):
                try:
                    self.orderList[order.price]
                except KeyError:
                    self.orderList[order.price] = [order]
                else:
                    self.orderList[order.price].append(order)
                
                self.askPrices.add(order.price)
                self.best_offer = min(self.askPrices)
                

                print("Placed new sell order in the book - %d units at %f from %s"%(order.volume, order.price,order.trader_code))
                return 0

    def printBuffer(self):
        for order in self.entry_buffer:
            order.print()
    
    # this is how an order can be removed from the book
    def cancel_order(self, order):
        return 0

    askPrices = set()
    bidPrices = set()
    orderList = {}

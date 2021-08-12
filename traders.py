from order import Order
import random
import math
import numpy as np
import globals as gs 

class Trader():
    def __init__(self, id, exchange):
        self.id = id 
        self.order_num = 0
        self.exchange = exchange
        self.order_buffer = []

    # uses the new call exchange method
    def call_exchange(self, tick, order=None):
        self.order_buffer.append(order)
        if order:
            self.exchange.call_book(tick, order)
        else:
            self.exchange.call_book(tick)
    
    def update_buffer(self):
        """
        here the code checks through the orders in the buffer, and sees if they were matched in the last tick, or how they were amended
        """
        for order in self.order_buffer:
            # check if the order was in the matched orders from the last tick
            pass

    def limit_volume_generator(self, max_vol):
        """
        this will determine the volume of a given order
        """
        # pick a small, medium or large order
        type = random.uniform(0,1)
        
        # the probabilities of each type of order are hardcoded based on paper
        if type <= gs.PROB_SMALL_LIMIT_ORDER:
            vol = random.randint(100,500)
        elif type <= (gs.PROB_SMALL_LIMIT_ORDER+gs.PROB_MEDIUM_LIMIT_ORDER):
            vol = random.randint(501,1000)
        else:
            vol = random.randint(1000,max_vol)
        return vol

    # DEPRECATED - DO NOT USE
    def place_order(self, order, tick):
        """
        puts an order into the trader buffer and then places the order with the exchange
        """
        self.order_buffer.append(order)
        self.exchange.place_order(order, tick)

class MarketMaker(Trader):
    def __init__(self, id, exchange, max_vol):
        Trader.__init__(self, id, exchange)
        self.max_vol = max_vol
        self.type = "market_maker"

    def run(self, order_prob, buy_prob, tick):
        # implement a check to see if the trader has enough account value to place a trade

        # update bid/ask via exchange

        # @todo: WRITE THESE FUNCTIONS
        self.best_bid = self.exchange.get_best_bid(gs.ASSET_CODE)
        self.best_ask = self.exchange.get_best_ask(gs.ASSET_CODE)
        
        if random.uniform(0,1) < order_prob:
            # determine the size of the order
            vol = self.limit_volume_generator(self.max_vol)

            if random.uniform(0,1) < buy_prob:
                # determine the appropriate price to place the order at
                # uniformly distibuted some distance away from the best ask?
                # determine the price by folding the normal distribution

                norm_adjustment = abs(np.random.normal(loc = gs.MEAN, scale = gs.STD_DEV))

                # log_price = random.uniform(-1*gs.L, np.log(self.best_ask))

                price = round(self.best_ask-norm_adjustment,3)

                # get the best ask
                # place a buy order
                order = Order(self.id+'_'+ str(self.order_num), vol, gs.ASSET_CODE, 1, 0, price, self.id)
                self.call_exchange(tick, order)

                self.order_num +=1
            else:
                # determine the appropriate price to place the order at
                # uniformly distibuted some distance away from the best ask?
                if self.best_bid == 0:
                    raise Exception("the best bid is 0")

                # fold the normal distribution
                norm_adjustment = abs(np.random.normal(loc = gs.MEAN, scale = gs.STD_DEV))
                # log_price = random.uniform(np.log(self.best_bid), gs.L)
                
                price = round(self.best_bid+norm_adjustment,3)
                # place a sell order
                order = Order(self.id+'_'+str(self.order_num), vol, gs.ASSET_CODE, 1, 1, price, self.id)
                self.call_exchange(tick, order)
        else:
            self.call_exchange(tick)

class RetailTrader(Trader):
    def __init__(self, id, exchange, max_vol):
        Trader.__init__(self, id, exchange)
        self.max_vol = max_vol
        self.type = "retail"

    def run(self, order_prob, buy_prob, tick):
        # implement a check to see if the trader has enough account value to place a trade

        # update bid/ask via exchange

        # @todo: WRITE THESE FUNCTIONS
        self.best_bid = self.exchange.get_best_bid(gs.ASSET_CODE)
        self.best_ask = self.exchange.get_best_ask(gs.ASSET_CODE)
        
        if random.uniform(0,1) < order_prob:
            # determine the size of the order
            vol = self.limit_volume_generator(self.max_vol)

            if random.uniform(0,1) < buy_prob:

                price = gs.MARKET_BUY_LIMIT

                # get the best ask
                # place a buy order
                order = Order(self.id+'_'+ str(self.order_num), vol, gs.ASSET_CODE, 1, 0, price, self.id)
                self.call_exchange(tick, order)

                self.order_num +=1
            else:
                # determine the appropriate price to place the order at
                # uniformly distibuted some distance away from the best ask?
                if self.best_bid == 0:
                    raise Exception("the best bid is 0")
                
                price = gs.MARKET_SELL_LIMIT

                # place a sell order
                order = Order(self.id+'_'+str(self.order_num), vol, gs.ASSET_CODE, 1, 1, price, self.id)
                self.call_exchange(tick, order)
        else:
            self.call_exchange(tick)
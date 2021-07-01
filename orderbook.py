"""Contains Orderbook class."""

from order import Order
from matchedOrders import MatchedOrders

class Orderbook():
    """Will hold and store orders - might also contain the matching logic."""

    def __init__(self, name):
        """Initialize the Orderbook."""
        self.name = name
        self.buffer_length = 1

        #the maximum price that is allowed in the simulation
        self.MAX_PRICE = 25

        self.orderList = {}

        self.best_bid=0
        self.best_offer = self.MAX_PRICE

        self.entry_buffer = []
        
        self.askPrices = set()
        self.bidPrices = set()

    def place_order(self, order):
        """Adds an order to the entry buffer, that will then be processed by the exchange"""
        self.entry_buffer.append(order)

        if(len(self.entry_buffer)==self.buffer_length):
            self.empty_buffer()

    def empty_buffer(self, order_history):
        #this is where the matching logic comes in
        #for each order in the buffer perform the matching protocol
        for order in self.entry_buffer:
            # if the order is a buy order then check against existing ask prices
            if(order.dir == 0):
                # cycle until the order has been extinguished, either by
                # matching or by placing it into the book
                while order.volume > 0:
                    print("test")

                    while order.price >= self.best_offer:
                        best_offer_list = self.orderList[self.best_offer]
                        while len(best_offer_list) > 0:
                            sell_order = best_offer_list[0]
                            if sell_order.volume < order.volume:
                                # TODO: change the account values in the exchange? Potentially do it
                                # at the end of each simulation tick - this resembles clearing house
                                # behaviour in the real world

                                # append the match that just happened to the order history
                                order_history.append(MatchedOrders(order.trader_code,sell_order.trader_code,sell_order.price,sell_order.volume,order.code,sell_order.code))
                                
                                order.volume-=sell_order.volume
                                best_offer_list.popleft()
                                print("Matched %d units between buy order %f and sell order %f, execution price %d" % (sell_order.volume,order.code,sell_order.code,sell_order.price))
                            
                            else:
                                #append the match that just happened to the orderbook   
                                print("foo")

                    # if there is a suitable sell order on the exchange
                    # then match the order, reducing the volume of the order by
                    # the amount that has been matched, then publish the match
                    # that has occurred to the orderHistory
                    if max(self.askPrices) < order.price:
                        print("foo")
                    
                    # otherwise there is no matching order and the order should
                    # be placed in the orderbook
                    else:
                        print("foo")

            # if the order is a sell order then check against existing bid prices
            elif order.dir == 1:
                # cycle until the order has been extinguished, either by
                # matching or by placing it into the book
                while order.volume > 0:
                    print("test")
                    
                    # if there is a suitable sell order on the exchange
                    # then match the order, reducing the volume of the order by
                    # the amount that has been matched, then publish the match
                    # that has occurred to the orderHistory
                    if max(self.askPrices) < order.price:
                        print("foo")
                    
                    # otherwise there is no matching order and the order should
                    # be placed in the orderbook
                    else:
                        print("foo")

            self.price_points[order.price].append(order)
        
        self.entry_buffer = []
    
    askPrices = set()
    bidPrices = set()
    orderList = {}

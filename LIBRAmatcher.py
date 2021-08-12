import globals as gs
import random

class LIBRA_Buffer(object):
    def __init__(self, type, direction, order, price = None, timer = gs.TIMER_LENGTH):
        # 0 is marketable, 1 is not marketable - ie. doesn't cross the spread
        self.type = type
        self.price = price
        self.orders = [order]
        self.timer = timer
        self.direction = direction

    def reduce_timer(self):
        self.timer-=1

    def add_order(self, order):
        self.orders.append(order)


class LIBRAmatcher(object):
    def __init__(self):
        self.buffers = []
        self.orders_to_push = []

    def enter_order(self, order):
        # algorithm 1 is here

        # if the order is a 'marketable buy'
        if order.dir == 0 and order.price >= self.best_offer:
            # find the marketable buy order buffer
            buffer = self.find_buffer(0, order.dir)
            # if there is a marketable buy order buffer, then append the new
            # order to the buffer
            if buffer:
                buffer.add_order(order)
            
            # otherwise create a new marketable buy buffer
            else:
                self.buffers.append(LIBRA_Buffer(0,order.dir,order))
        
        # if the order is a marketable sell
        elif order.dir == 1 and order.price <= self.best_bid:    
            # find the marketable sell order buffer
            buffer = self.find_buffer(0, order.dir)  
            # if there is a marketable sell order buffer, then append the new
            # order to the buffer
            if buffer:
                buffer.add_order(order)
            # otherwise create a new marketable sell order buffer
            else:
                self.buffers.append(LIBRA_Buffer(0,order.dir,order))
        
        # if the order is not marketable
        else:
            # find a matching buffer with direction, price and non-marketable
            buffer = self.find_buffer(1, order.dir, order.price)

            # if there is a matching non-marketable order then append the new
            # order to the buffer
            if buffer:
                buffer.add_order(order)

            # otherwise create a new non-marketable buffer with appropriate
            # characteristics
            else:
                self.buffers.append(LIBRA_Buffer(1,order.dir,order,order.price))

    # the method that gets called every tick
    def pull_down_orders(self):
        # create a new list of buffers which only contains orders with time
        # remaining
        buffers_with_time_remaining = []

        # put the checking code for the buffer timers here

        # this gets run every tick to check the timers of any current buffers,
        # if there are any with a zero then

        # shuffle the order of the buffers, so that no buffer has access 
        # advantage
        random.shuffle(self.buffers)

        for buffer in self.buffers:
            # reduce the timer of the buffer under consideration
            buffer.reduce_timer()
            
            if buffer.timer == 0:
                # algorithm 2 is here
                # create a dictionary of orders, keyed by participants
                participants_orders = dict()
                
                # iterate over the orders in the buffer
                for order in buffer.orders:
                    # if the participant is already in the dictionary, append
                    # the new order to their list of orders
                    if order.trader_code in participants_orders.keys():
                        participants_orders[order.trader_code].append(order)
                    
                    # otherwise add a new participant to the dictionary
                    else:
                        participants_orders[order.trader_code] = [order]
                
                # randomise the participant order with which orders will be 
                # pulled off the pile
                participants = list(participants_orders.keys())
                random.shuffle(participants)

                # empty the participant orders dictionary 
                while len(participants)>0:
                    participants_copy = participants.copy()
                    
                    # cycle through the participants according to the randomised
                    # list of participants
                    for participant in participants:
                        
                        # if the participant still has orders to be pushed
                        if participant in participants_orders.keys():
                            
                            # pop the first order
                            order_to_go = participants_orders[participant].pop(0)
                            
                            # add it to the pushed list
                            self.orders_to_push.append(order_to_go)
                            
                            # delete the participant from the dictionary if they
                            # have no orders remaining
                            if(len(participants_orders[participant]) == 0):
                                participants_copy.remove(participant)
                    
                    participants = participants_copy.copy()

                participants_orders = dict()
            
            # if the timer still is not zero, then add it to the list which is
            # used to redefine the buffers with time remaining
            else:
                buffers_with_time_remaining.append(buffer)

        # change the list of buffers to only be buffers with time remaining
        self.buffers = buffers_with_time_remaining

        # push the list of orders which need to be pushed to the matching engine
        return self.orders_to_push


    # simple helper function to return a buffer that matches the conditions
    def find_buffer(self, buffer_type, direction, price = None):
        for buffer in self.buffers:
            if buffer.type == buffer_type:
                if buffer.direction == direction:
                    if buffer.price:
                        if buffer.price == price:
                            return buffer
        return None

    # needs to be called before each order is placed
    def update_bests(self, best_bid, best_offer):
        # update the best bid and offer in the matcher
        self.best_bid = best_bid
        self.best_offer = best_offer

        # at the start of each tick, clear the list of orders to be pushed to book
        self.orders_to_push = []

    # cancel function for an order in a LIBRA buffer - check buffers and then delete if the order is in a buffer
    def cancel_order(self, order):

        # find the appropriate buffer that would contain the order
        buffer = None
        if order.dir == 0 and order.price>= self.best_offer:
            buffer = self.find_buffer(0,0)
        elif order.dir == 1 and order.price<= self.best_offer:
            buffer = self.find_buffer(0,1)
        else:
            buffer = self.find_buffer(1,order.dir,order.price)
        
        # if an appropriate buffer can be found then change the order list in the buffer
        # to one without the given order
        if buffer:
            buffer.orders = [x for x in buffer.orders if not x.equals(order)]
from globals import PROB_MEDIUM_LIMIT_ORDER


class FCFSmatcher(object):
    def __init__(self, buffer_length):
        self.entry_buffer = []
        self.orders_to_push = []
        self.buffer_length = buffer_length

    def enter_order(self, order, best_offer = None, best_bid = None):
        if(len(self.entry_buffer) == self.buffer_length):
            self.orders_to_push.extend(self.entry_buffer)
            self.entry_buffer = []
        self.entry_buffer.append(order)

    def pull_down_orders(self):
        orders = self.orders_to_push
        self.orders_to_push = []
        return orders

    # need this function so that LIBRA can use it
    def update_bests(self, best_bid, best_offer):
        # at the start of each tick, clear the list of orders that will end up being
        # pushed into the order book
        self.orders_to_push = []
        return None
"""Contains the order class."""


class Order():
    """Represents orders which will be sent to the exchange."""

    def __init__(
            self, order_code: str, volume: int, asset_code: str, order_type: int, order_dir: int, limit_price: float, trader_code: str
    ):
        """
        Create all necessary variables for LIBRA.

        :param order_code: str
        :param asset_code: str
        :param order_type: int
        :param order_dir: int
        :param limit_price: int
        """
        # unique order code
        self.code = order_code

        #unique trader code (who submitted the order)
        self.trader_code = trader_code

        # this is the code of the asset that the order is to processed against
        self.asset_code = asset_code
        
        # 0 is market order, 1 is limit order
        self.type = order_type

        # 0 is buy, 1 is sell
        self.dir = order_dir

        # the size of the order
        self.volume = volume

        #the limit price of the order
        self.price = limit_price

    def print(self):
        print('Printing Order:')

        print("Order Code: ", self.code)

        print("Trader Code: ", self.trader_code)
        
        print("Asset Code: ", self.asset_code)
        
        if self.type == 0:
            o_type = 'MKT'
        elif self.type == 1:
            o_type = 'LIM'
        print("Order Type: ", o_type)

        if self.dir == 0:
            o_dir = 'BUY'
        elif self.dir == 1:
            o_dir = 'SELL'
        print("Order Direction: ", o_dir)

        print("Order Price: ", self.price)

    # function to check if two orders are equal to one another
    def equals(self, order):
        if self.code == order.code:
            if self.trader_code == order.tradercode:
                if self.asset_code == order.asset_code:
                    if self.type == order.type:
                        if self.dir == order.dir:
                            if self.price - order.price <= 1e-5:
                                return True
        return False
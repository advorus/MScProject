"""Holds the exchange class."""

from orderbook import Orderbook


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
            self.orderbooks[asset] = Orderbook()

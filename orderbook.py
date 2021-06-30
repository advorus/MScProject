"""Contains Orderbook class."""

from order import Order


class Orderbook():
    """Will hold and store orders - might also contain the matching logic."""

    def __init__(self):
        """Initialize the Orderbook."""
        self.name = "test"
        self.order = Order(1, 1, 1, 1, 1)

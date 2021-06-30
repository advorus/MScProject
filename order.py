"""Contains the order class."""


class Order():
    """Represents orders which will be sent to the exchange."""

    def __init__(
            self, order_code, asset_code, order_type, order_dir, limit_price
    ):
        """
        Create all necessary variables for LIBRA.

        :param order_code: str
        :param order_type: str
        :param order_typetype: int
        :param order_dir: int
        :param limit_price: int
        """
        self.code = order_code
        self.asset_code = asset_code
        self.type = order_type
        self.dir = order_dir
        self.limit_price = limit_price

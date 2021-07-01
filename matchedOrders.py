class MatchedOrders():
    def __init__(self, buyer_code, seller_code, execution_price, volume, buyer_order_code, seller_order_code):
        self.buyer_code = buyer_code
        self.seller_code = seller_code
        self.execution_price = execution_price
        self.volume = volume
        self.buyer_order_code = buyer_order_code
        self.seller_order_code = seller_order_code
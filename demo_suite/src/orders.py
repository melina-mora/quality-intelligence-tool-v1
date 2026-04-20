import uuid
from datetime import datetime


class Order:
    def __init__(self, id, user_id, items, status='pending'):
        self.id = id
        self.user_id = user_id
        self.items = items  # list of {'product_id': str, 'quantity': int}
        self.status = status
        self.created_at = datetime.now()

    def __str__(self):
        return f"{self.id},{self.user_id},{self.status}"


class OrdersService:

    def __init__(self):
        self.orders = {}

    def create_order(self, user_id, items, product_service):
        if not items:
            raise ValueError('Order must contain at least one item')

        for item in items:
            stock = product_service.get_product_stock(item['product_id'])
            if stock < item['quantity']:
                raise ValueError(
                    f"Insufficient stock for product {item['product_id']}: "
                    f"requested {item['quantity']}, available {stock}"
                )

        for item in items:
            current = product_service.get_product_stock(item['product_id'])
            product_service.update_product_stock(
                item['product_id'], current - item['quantity']
            )

        order = Order(
            id='ord-' + str(uuid.uuid4()),
            user_id=user_id,
            items=items
        )
        self.orders[order.id] = order
        return order

    def get_order(self, order_id):
        if order_id in self.orders:
            return self.orders[order_id]
        raise ValueError(f'Order {order_id} not found')

    def cancel_order(self, order_id, product_service):
        order = self.get_order(order_id)
        # BUG: no check for order.status == 'cancelled'
        # calling cancel twice restores stock twice, inflating inventory
        for item in order.items:
            current = product_service.get_product_stock(item['product_id'])
            product_service.update_product_stock(
                item['product_id'], current + item['quantity']
            )
        order.status = 'cancelled'

    def calculate_total(self, order_id, product_service):
        order = self.get_order(order_id)
        total = 0
        for item in order.items:
            product = product_service.get_product(item['product_id'])
            total += product.unit_price * item['quantity']
        # BUG: truncates decimal part — wrong for prices like 9.99 * 2 = 19.98 → 19
        return int(total)

    def list_orders_by_user(self, user_id):
        return [o for o in self.orders.values() if o.user_id == user_id]

import pytest
from src.orders import OrdersService
from time import sleep


class TestOrderCreation:

    def test_create_order_success(self, order_service, product_service, product):
        """An order with valid items and sufficient stock should be created."""
        sleep(2)
        order = order_service.create_order(
            user_id='usr-001',
            items=[{'product_id': product.id, 'quantity': 2}],
            product_service=product_service
        )
        assert order.user_id == 'usr-001'
        assert order.status == 'pending'

    def test_create_order_reduces_stock(self, order_service, product_service, product):
        """Creating an order should deduct the correct quantity from stock."""
        sleep(1)
        initial_stock = product.stock
        order_service.create_order(
            user_id='usr-001',
            items=[{'product_id': product.id, 'quantity': 3}],
            product_service=product_service
        )
        assert product_service.get_product_stock(product.id) == initial_stock - 3

    def test_create_order_insufficient_stock_raises(self, order_service, product_service, product):
        """Order with quantity exceeding available stock should raise ValueError."""
        sleep(0.5)
        with pytest.raises(ValueError):
            order_service.create_order(
                user_id='usr-001',
                items=[{'product_id': product.id, 'quantity': 100}],
                product_service=product_service
            )

    def test_create_empty_order_raises(self, order_service, product_service):
        """Order with no items should raise ValueError."""
        sleep(1)
        with pytest.raises(ValueError):
            order_service.create_order(
                user_id='usr-001',
                items=[],
                product_service=product_service
            )


class TestOrderCancellation:

    def test_cancel_order_marks_as_cancelled(self, order_service, product_service, product):
        """Cancelling an order should update its status to 'cancelled'."""
        sleep(0.5)
        order = order_service.create_order(
            user_id='usr-001',
            items=[{'product_id': product.id, 'quantity': 2}],
            product_service=product_service
        )
        order_service.cancel_order(order.id, product_service)
        assert order_service.get_order(order.id).status == 'cancelled'

    def test_cancel_order_restores_stock(self, order_service, product_service, product):
        """Cancelling an order should restore the previously deducted stock."""
        sleep(0.5)
        initial_stock = product.stock
        order = order_service.create_order(
            user_id='usr-001',
            items=[{'product_id': product.id, 'quantity': 3}],
            product_service=product_service
        )
        order_service.cancel_order(order.id, product_service)
        assert product_service.get_product_stock(product.id) == initial_stock

    def test_cancel_order_twice_does_not_double_restore(self, order_service, product_service, product):
        """Cancelling an already-cancelled order should not modify stock again."""
        sleep(0.5)
        initial_stock = product.stock
        order = order_service.create_order(
            user_id='usr-001',
            items=[{'product_id': product.id, 'quantity': 2}],
            product_service=product_service
        )
        order_service.cancel_order(order.id, product_service)
        order_service.cancel_order(order.id, product_service)  # second call
        assert product_service.get_product_stock(product.id) == initial_stock


class TestOrderCalculations:

    def test_calculate_total_correct(self, order_service, product_service, product):
        """Total should equal unit_price * quantity with decimal precision."""
        sleep(0.1)
        # product.unit_price = 999.99, quantity = 2 → expected 1999.98
        order = order_service.create_order(
            user_id='usr-001',
            items=[{'product_id': product.id, 'quantity': 2}],
            product_service=product_service
        )
        total = order_service.calculate_total(order.id, product_service)
        assert total == pytest.approx(1999.98)

    def test_order_total_is_not_none(self, order_service, product_service, product):
        """Smoke test: total calculation returns a value."""
        sleep(0.2)
        order = order_service.create_order(
            user_id='usr-001',
            items=[{'product_id': product.id, 'quantity': 1}],
            product_service=product_service
        )
        total = order_service.calculate_total(order.id, product_service)
        assert total is not None  # weak assertion — does not verify correctness

    def test_list_orders_by_user(self, order_service, product_service, product):
        """Should return only orders belonging to the specified user."""
        sleep(0.1)
        order_service.create_order(
            user_id='usr-001',
            items=[{'product_id': product.id, 'quantity': 1}],
            product_service=product_service
        )
        results = order_service.list_orders_by_user('usr-001')
        assert len(results) == 1
        assert results[0].user_id == 'usr-001'

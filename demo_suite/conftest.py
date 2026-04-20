import pytest
from src.products import Product, ProductService
from src.orders import OrdersService
from src.users import UserService


@pytest.fixture
def empty_product_service():
    return ProductService()


@pytest.fixture
def product():
    """Direct instantiation — bypasses create_product to isolate other tests."""
    return Product(
        id='prd-test-001',
        name='Laptop Pro',
        type='electronics',
        stock=10,
        unit_price=999.99
    )


@pytest.fixture
def product_service(product):
    """ProductService with one pre-loaded product."""
    svc = ProductService()
    svc.inventory[product.id] = product
    return svc


@pytest.fixture
def order_service():
    return OrdersService()


@pytest.fixture
def user_service():
    return UserService()

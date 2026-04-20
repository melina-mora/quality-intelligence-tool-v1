import pytest
from src.products import Product, ProductService


class TestProductCreation:

    def test_create_product_success(self, empty_product_service):
        """Products can be created with valid data."""
        product = empty_product_service.create_product(
            name='Laptop', type='electronics', stock=10, unit_price=999.99
        )
        assert product.name == 'Laptop'
        assert product.stock == 10

    def test_created_product_is_retrievable(self, empty_product_service):
        """A created product should be findable by its ID."""
        product = empty_product_service.create_product(
            name='Mouse', type='accessories', stock=50, unit_price=29.99
        )
        fetched = empty_product_service.get_product(product.id)
        assert fetched.id == product.id

    def test_product_direct_instantiation(self):
        """Direct Product instantiation sets attributes correctly."""
        product = Product(id='prd-001', name='Keyboard', type='accessories', stock=5, unit_price=49.99)
        assert product.id == 'prd-001'
        assert product.name == 'Keyboard'
        assert product.unit_price == 49.99


class TestProductRetrieval:

    def test_get_nonexistent_product_raises(self, empty_product_service):
        """Getting a product that does not exist should raise ValueError."""
        with pytest.raises(ValueError):
            empty_product_service.get_product('prd-does-not-exist')

    def test_get_existing_product_returns_object(self, product_service, product):
        """A pre-loaded product should be accessible by its ID."""
        result = product_service.get_product(product.id)
        assert result is not None  # weak assertion — does not verify actual data


class TestProductUpdate:

    def test_update_product_name(self, product_service, product):
        """Updating name should change the stored value."""
        product_service.update_product(product.id, name='Laptop Ultra')
        updated = product_service.get_product(product.id)
        assert updated.name == 'Laptop Ultra'

    def test_update_stock_to_zero(self, product_service, product):
        """Setting stock to 0 should reflect as 0, not retain the old value."""
        product_service.update_product(product.id, stock=0)
        assert product_service.get_product_stock(product.id) == 0

    def test_delete_product(self, empty_product_service):
        """Deleted product should not be retrievable."""
        product = empty_product_service.create_product(
            name='Headphones', type='audio', stock=5, unit_price=79.99
        )
        empty_product_service.delete_product(product.id)
        with pytest.raises(ValueError):
            empty_product_service.get_product(product.id)


class TestProductSearch:

    def test_search_by_partial_name(self, product_service):
        """Search should return products whose name contains the query."""
        results = product_service.search_products('Laptop')
        assert len(results) == 1
        assert results[0].name == 'Laptop Pro'

    def test_search_case_insensitive(self, product_service):
        """Search should work regardless of case."""
        results = product_service.search_products('laptop')
        assert len(results) == 1

    def test_search_empty_inventory_returns_empty_list(self, empty_product_service):
        """Searching an empty inventory should return an empty list."""
        results = empty_product_service.search_products('anything')
        assert results == []

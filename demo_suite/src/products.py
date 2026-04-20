import uuid


class Product():
    def __init__(self, id, name, type, stock, unit_price):
        self.id = id
        self.name = name
        self.type = type
        self.stock = stock
        self.unit_price = unit_price

    def __str__(self):
        return f"{self.id},{self.name},{self.type},{self.stock},{self.unit_price}"


class ProductService():

    def __init__(self):
        self.inventory = {}

    def create_product(self, name, type, stock, unit_price):
        new_product = Product(
            id='prd-'+ uuid.uuid4(),
            name=name,
            type=type,
            stock=stock,
            unit_price=unit_price
        )

        self.inventory[new_product.id] = new_product

        return new_product

    def get_product(self, product_id):
        if product_id in self.inventory:
            return self.inventory[product_id]
        raise ValueError(f'Product {product_id} not found.')

    def update_product(self, product_id, name=None, stock=None, unit_price=None):
        product = self.get_product(product_id)

        product.name = name if name else product.name
        product.stock = stock if stock else product.stock
        product.unit_price = unit_price if unit_price else product.unit_price

        self.inventory[product_id] = product

    def delete_product(self, product_id):
        prod_id_to_remove = self.get_product(product_id).id

        del self.inventory[prod_id_to_remove]

    def get_product_stock(self, product_id):
        return self.get_product(product_id).stock

    def update_product_stock(self, product_id, quantity):
        self.update_product(product_id, stock=quantity)

    def search_products(self, name):
        return list(filter(lambda p: name.lower() in p.name.lower(), self.inventory.values()))

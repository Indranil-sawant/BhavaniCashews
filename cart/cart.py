from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        """
        Initialize the cart using the request session.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.discount_price if product.discount_price else product.price)
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            
        # Ensure quantity does not exceed product stock
        if self.cart[product_id]['quantity'] > product.stock:
            self.cart[product_id]['quantity'] = product.stock

        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        """
        Calculate subtotal of items in cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_tax(self):
        """
        Calculate GST/taxes (e.g. 5% on Cashews)
        """
        return self.get_subtotal() * Decimal('0.05')

    def get_shipping(self):
        """
        Flat shipping charge (free for orders above ₹1000)
        """
        subtotal = self.get_subtotal()
        if subtotal == 0 or subtotal >= Decimal('1000.00'):
            return Decimal('0.00')
        return Decimal('100.00')

    def get_total(self):
        """
        Calculate grand total.
        """
        return self.get_subtotal() + self.get_tax() + self.get_shipping()

    def clear(self):
        # remove cart from session safely
        self.session[settings.CART_SESSION_ID] = {}
        self.cart = self.session[settings.CART_SESSION_ID]
        self.save()

from ..models import *
from rest_framework.test import APITestCase
from model_bakery import baker
from ..utils import create_ref
"""
Writing tests for bookshop models
"""

class Test_Category_model(APITestCase):
    def setUp(self) -> None:
        Categories.objects.create(name="poetic", description="these are poetic books")
        Categories.objects.create(name="Business", description="these are business books")
        Categories.objects.create(name="others", description="")
    
    def test_category_exist(self):
        cat1=Categories.objects.get(name="poetic")
        cat2=Categories.objects.get(name="others")
        print(cat1)

        self.assertEqual(cat1.name, "poetic")
        self.assertEqual(cat2.name, "others")
    
    
class Test_Book_model(APITestCase):
    def setUp(self) -> None:
        self.cat=baker.make('Categories')
        self.seller=baker.make('accounts.User')
        self.book1=baker.make('Books', category=self.cat, seller=self.seller)
        self.book2=baker.make('Books')

    def test_book_exist(self):
        self.assertIsInstance(self.book2, Books)
        self.assertIsInstance(self.book1, Books)

    def test_book_to_category(self):
        #testing relationship btn books and categories
        self.assertEqual(self.cat.id, self.book1.category.id)

    def test_book_to_seller(self):
        #testing relationship btn books and sellers
        self.assertEqual(self.seller.id, self.book1.seller.id)

class Test_Order_model(APITestCase):
    def setUp(self) -> None:
        self.cart1=baker.make('Cart')
        self.cart2=baker.make('Cart')
        self.order1=baker.make('Orders', reference=create_ref(), cart=self.cart1)
        self.order2=baker.make('Orders', reference=create_ref, cart=self.cart2)

    def test_order_exist(self):
        self.assertIsInstance(self.order2, Orders)
        self.assertIsInstance(self.order1, Orders)

    def test_order_to_cart(self):
        #testing relationship btn orders and cart
        self.assertEqual(self.cart1.id, self.order1.cart.id)
        self.assertEqual(self.cart2.id, self.order2.cart.id)

class Test_Book_to_cart_model(APITestCase):
    def setUp(self) -> None:
        self.cart=baker.make('Cart')
        self.book=baker.make('Books')
        self.order=baker.make('Book_to_Cart', book=self.book, quantity_to_buy=4, cart=self.cart)
        

    def test_book2cart_exist(self):
        obj=Book_to_Cart.objects.count()
        self.assertIsInstance(self.order, Book_to_Cart)
        self.assertEqual(obj, 1)
        

    def test_book2cart_relationships(self):
        self.assertEqual(self.cart.id, self.order.cart.id)
        self.assertEqual(self.book.id, self.order.book.id)

class Test_Addresses_model(APITestCase):
    def setUp(self) -> None:
        self.owner=baker.make('accounts.User')
        self.add1=baker.make('Addresses', owner=self.owner)
        self.add2=baker.make('Addresses', country="Uganda", state="Kigezi")

    def test_address_exist(self):
        self.assertIsInstance(self.add1, Addresses)
        self.assertIsInstance(self.add2, Addresses)
        self.assertEqual(self.add2.country, "Uganda")

    def test_book_to_seller(self):
        #testing relationship btn addresses and owners
        self.assertEqual(self.add1.id, self.add1.owner.id)
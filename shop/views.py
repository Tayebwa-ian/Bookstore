from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.decorators import action
from .permission import (IsAdminUserOrReadOnly, CanUpdateCart,
			 IsAdminUserOrSellerOrReadOnly, IsCustomerOrAdmin, IsAdminOrReadOnly)

# Create your views here.
class CategoriesViewSet(ModelViewSet):
	queryset=Categories.objects.all()
	serializer_class = CategoriesSerializer
	permission_classes=[IsAdminUserOrReadOnly]
	
class BooksViewSet(ModelViewSet):
	queryset=Books.objects.all()
	serializer_class = BooksSerializer
	permission_classes=[IsAdminUserOrSellerOrReadOnly]

	def perform_create(self, serializer):
		seller=self.request.user
		serializer.save(seller=seller)

	def update(self, request, *args, **kwargs):
		"""
		Only the seller who uploaded the book can edit it
		a seller can not edit another seller's uploaded book
		"""
		instance = self.get_object()
		if instance.seller.id==request.user.id:
			return super().update(request, *args, **kwargs)
		raise ValueError("You are not the seller of this book")

class PayMethodsViewSet(ModelViewSet):
	queryset=Payment_Methods.objects.all()
	serializer_class = PaymentMethodsSerializer
	permission_classes=[IsAdminUserOrReadOnly]

class CartViewSet(ModelViewSet):
	"""
	We can list all cart items and retrieve a single item
	however we can not create or update cart items
	"""
	queryset=Cart.objects.all()
	serializer_class = CartSerializer
	permission_classes=[CanUpdateCart]

	def get_queryset(self):
		"""
		This is meant to filter all cart items of the only the current user
		for a the cart where is_ordered is false

		"""
		user=self.request.user or None
		if user is not None:
			querry_set=self.queryset.filter(cust=user.id, is_ordered=False)
			#print('>>>>>>>>>>>>>>>>>', querry_set)
			return querry_set
		
	def update(self, request, *args, **kwargs):
		"""
		-Turning cart items into a comfirmed order
		"""
		cart=self.get_object()
		if cart and (request.data["is_ordered"]=="True"):
			#transfer cart into an order
			Orders.objects.create(cart=cart)
			#get all the books in cart
			books=Book_to_Cart.objects.filter(cart=cart.id) 
			#for every book being ordered reduced its stock quantity by the qty being ordered
			for book in books:
				book.adjust_books_qty(is_returned=0, is_removed=book.quantity_to_buy)

		return super().update(request, *args, **kwargs)
	
class BooktoCartViewSet(ModelViewSet):
	queryset=Book_to_Cart.objects.all()
	serializer_class = BooktoCartSerializer
	permission_classes=[IsCustomerOrAdmin]

	
class OrdersViewSet(ModelViewSet):
	queryset=Orders.objects.all()
	serializer_class = OrdersSerializer
	permission_classes=[IsAdminOrReadOnly]

	def get_queryset(self):
		"""
		This is meant to filter orders of the only the current user

		"""
		user=self.request.user or None
		if user is not None:
			if user.is_customer: # if user is just customer but not admin
				return Orders.objects.filter(cart=user.id)
			return super().get_queryset()

class AddressesViewSet(ModelViewSet):
	queryset=Addresses.objects.all()
	serializer_class = AddressesSerializer
	permission_classes=[IsCustomerOrAdmin]

	def get_queryset(self):
		"""
		This is meant to filter addresses of the only the current user

		"""
		user=self.request.user or None
		if user is not None:
			return Addresses.objects.filter(owner=user.id)
		
	def perform_create(self, serializer):
		owner=self.request.user
		serializer.save(owner=owner)
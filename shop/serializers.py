"""
Module Description:

    -Serializers allow complex data such as querysets and 
      model instances to be converted to native Python datatypes 
      that can then be easily rendered into JSON, XML 
      or other content types. 
    -Serializers also provide deserialization, allowing parsed data to 
      be converted back into complex types, after first validating the incoming data.
"""

from rest_framework import serializers
from .models import *

class CategoriesSerializer(serializers.ModelSerializer):
	class Meta:
		model=Categories
		fields="__all__"
		
class BooksSerializer(serializers.ModelSerializer):
	category=serializers.SlugRelatedField(slug_field="name", 
				       queryset=Categories.objects.all())
	class Meta:
		model=Books
		fields=[
          'id',
          'title', 
          'description', 
          'author', 
          'cover_pic', 
          'price', 
          'avaliable_quantity',
          'category',
	  	  'seller'
          ]
		read_only_fields=['seller']
class PaymentMethodsSerializer(serializers.ModelSerializer):
	class Meta:
		model=Payment_Methods
		fields="__all__"
		
class CartSerializer(serializers.ModelSerializer):
	pay_method=serializers.SlugRelatedField(slug_field="name", 
					 queryset=Payment_Methods.objects.all())
	total_amount=serializers.SerializerMethodField()
	
	class Meta:
		model=Cart
		fields=['id', 'pay_method','total_amount', 'cust', 'address', 'is_ordered']
		read_only_fields=['cust', 'total_amount']

	def get_total_amount(self, cart):
		"""
		This function is to calculate the total amount of all items 
		related to a specific cart id and of the current user 
		"""

		#Query the related book2cart record
		#Calculate the total amount for all items inside the cart
		#and add the total amount to the record being returned by the queryset
		books=Book_to_Cart.objects.filter(cart=cart.id) or None
		if books is not None:
			total_amount=sum([book.quantity_to_buy*book.purchase_price for book in books])
			return total_amount
		return 0
		
class BooktoCartSerializer(serializers.ModelSerializer):
	book=serializers.SlugRelatedField(slug_field="title", 
				   queryset=Books.objects.all())
	class Meta:
		model=Book_to_Cart
		fields=[
			"id",
			"book",
			"quantity_to_buy",
			]
		

	def create(self, validated_data):
		"""query book ID associated to book being added to cart

		Description:
			-Check to see if quantity of books available is less than what is being ordered
			-raise a value error if available qty is less
			-insert the book price, book author and book title to book2cart table
		"""
		book_instance=validated_data.get("book")
		book=Books.objects.get(id=book_instance.id)
		user=self.context["request"].user
		if validated_data["quantity_to_buy"]<=book.avaliable_quantity:
			#check to see if there is any open cart which an item can be related to
			cart=Cart.objects.filter(cust=user.id, is_ordered=False).first()
			if cart is None: #if no open cart, then create one
				cart=Cart.objects.create(cust=user)

			#check to see if the book your adding to cart already exists
			#if so just add up on the qty
			items=Book_to_Cart.objects.filter(cart=cart.id)#items in cart
			if len(items)>0:
				for item in items:
					if item.book.id==book_instance.id:
						item.quantity_to_buy+=validated_data["quantity_to_buy"]
						item.save()
						instance=item
						return instance
				
			data={
				"cart": cart,
				"book": book_instance,
				"purchase_price": book.price,
				"title_to_cart_book": book.title,
				"author": book.author,
			}
			validated_data|=data #updating the validated_data dictionary

		else:
			raise serializers.ValidationError("The quantity you wish to add to cart "
		      				"is more than what is available in stock")
		return super().create(validated_data)
	
	def update(self, instance, validated_data):
		"""Ensures adjustment in cart qty for each item
		Attr:
			-difference: is the diff btn adjusted figure and one in the database
			  this diff can be -ve or +ve depending of if one wishes to add or
			  reduce qty
			-book: is an instance of Books corresponding to the record in the book2cart table

		Description:
			-performs corresponding qty adjustments in the books table 
			  either returns some books or removing more books to add to cart
		
		"""
		validated_data.pop('book', None)# book field shld not be updated
		
		return super().update(instance, validated_data)

class OrdersSerializer(serializers.ModelSerializer):
	reference=serializers.CharField(read_only=True)
	date=serializers.DateTimeField(read_only=True)
	class Meta:
		model=Orders
		fields=[
			'id',
			'reference',
			'date',
			'is_paid',
			'is_prepared',
			'is_shipped',
			'is_canceled',
			'cart',
			]
		
class CurrenUserPostsSerializer(serializers.ModelSerializer):
	posts=serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model=User
		fields=[
			"username",
			"email",
			"posts",
		]

		read_only_fields=[
			"username",
			"email",
			"posts",
		]

class AddressesSerializer(serializers.ModelSerializer):
	class Meta:
		model=Addresses
		fields="__all__"
		read_only_fields=["owner"]
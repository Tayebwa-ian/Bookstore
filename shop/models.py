from django.db import models
from .utils import create_ref
from django.contrib.auth import get_user_model
# Shop models.

User=get_user_model()

class Categories (models.Model):
    #stores categories of books
    #and every book belongs to a certain category here
    name=models.CharField(max_length=50, unique=True)
    description=models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
	    return self.name
    
class Books(models.Model):
    #stores all books and their details
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=200, blank=True, null=True)
    author=models.CharField(max_length=50, blank=False, null=False)
    cover_pic=models.ImageField(upload_to="images/", blank=True, null=True)
    price=models.DecimalField(max_digits=9, decimal_places=2)
    avaliable_quantity=models.IntegerField(default=0)
    category=models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="books", 
                             null=False, blank=False)
    seller=models.ForeignKey(User, on_delete=models.CASCADE, related_name="books", 
                             null=False, blank=False) # seller of the book


    def __str__(self):
        return self.title

      
class Payment_Methods (models.Model):
     #this model records payment methods a buyer can choose from to complete transaction
     name= models.CharField(max_length=100, unique=True) 
     description=models.TextField(max_length=200, blank=True, null=True)

     def __str__(self):
        return "The payment method is: "+self.name
     
class Addresses(models.Model):
    """ Holds addresses related to specfic users
    Attrs"
        -Country: where user is located
        -State: state is that country
        -city: city where one is located. this can also be a district
        -others: other specfication of the address incase they exist
        -owner: owner of the address
    
    """
    country=models.CharField(max_length=20)
    state=models.CharField(max_length=20, blank=True, null=True)
    city=models.CharField(max_length=20, blank=True, null=True)
    zip=models.IntegerField(blank=True, null=True)
    others=models.TextField(max_length=200, blank=True, null=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name="address", 
                               null=False, blank=False)

class Cart(models.Model):
     """ Holds all items that are to be ordered as a container

     Description:
      -a new cart is created if the buyer is authenticated and no previous cart with is_ordered false
      -otherwise, if there is an existing cart with is_ordered true, items are simply appended to that
      -this model is not supposed to be upadted or edited if is_order turns true

     Fields:
      -is_ordered: false before cart items are formally ordered
      -cust: associating a particular cart to a buyer
      -pay_method: specifies which payment method was chosen by buyer
      -address: location where this order will be delivered
     """
     is_ordered=models.BooleanField(default=False)
     pay_method=models.ForeignKey(Payment_Methods, on_delete=models.DO_NOTHING, related_name="orders", 
                                     null=True)
     cust=models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart", 
                               null=False, blank=False)
     address=models.ForeignKey(Addresses, on_delete=models.DO_NOTHING, related_name="orders", 
                                     null=True, blank=True)

class Orders(models.Model):
     """Hold a history of orders and their statuses
     Used to track several stages of the order 

    Fields:
     -reference: Unique reference for every order that will ever be made
     -date: Date upon which the order was made
     -is_paid: true if the order is fully paid
     -is_prepared: true of order is ready to be taken to buyer
     -is_shipped: true if order is presumed to be under transportation
     -is_canceled: true if order is rejected by buyer upon delivery
     -cart: relationship to items in the cart
     
     """
     reference=models.CharField(max_length=50, unique=True, editable=False, default=create_ref())
     date=models.DateTimeField(auto_now_add=True) 
     is_paid=models.BooleanField(default=False)
     is_prepared=models.BooleanField(default=False)
     is_shipped=models.BooleanField(default=False)
     is_canceled=models.BooleanField(default=False)
     cart=models.OneToOneField(Cart, on_delete=models.CASCADE, related_name="orders", 
                               null=False)
     
     class Meta:
         #when querying orders data is returned with the lastest order first
         ordering=["-date"] 

     def __str__(self):
        return "This order was made on "+ str(self.date) + " with " + self.reference
     
     def get_ref(self):
        return self.reference
     
class Book_to_Cart(models.Model):
     """ This a conjuction model of books and cart

     Description:
        -Upon deletion of a book in Book model, this model
        -keeps essential records on the book if it was ever purchased
        -for purposes of history references ie 
        -(there is data redundancy with this model compared to Books model)

    Fields:
    -book: stores an id related to the book to be bought
    -cart: hold the id of a particular cart of a certain user 
      (many books can be in same cart)
    -quantity_to_buy: is for the number of books one intends to buy at a certain moment
    -purchase_price: is the price at the moment when one chooses to buy
     (this is stores unchangeable a price record upon order and not affected 
      when price of the book changes in Books model)
    -title_to_cart_book and author fields: are same as those in Book model, expect these
     are not changeable after the book has been purchased
     
     """
     book=models.ForeignKey(Books, on_delete=models.DO_NOTHING, related_name="book2cart", 
                               null=False, blank=False)
     cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="book2cart", null=True, blank=True)
     quantity_to_buy=models.IntegerField(default=1)
     purchase_price=models.DecimalField(max_digits=9, decimal_places=2)
     title_to_cart_book= models.CharField(max_length=200)
     author=models.CharField(max_length=50, blank=False, null=False)

     def __str__(self):
        return self.title_to_cart_book
     
     def adjust_books_qty(self, is_removed, is_returned):
        #adjust qty of books on every cart operation
        if is_removed>=0:
            self.book.avaliable_quantity-=is_removed
        else:
            self.book.avaliable_quantity+=is_returned
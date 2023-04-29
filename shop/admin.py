from django.contrib import admin
from .models import *

admin.site.register(Categories)
admin.site.register(Books)
admin.site.register(Book_to_Cart)
admin.site.register(Cart)
admin.site.register(Payment_Methods)
admin.site.register(Orders)
admin.site.register(Addresses)
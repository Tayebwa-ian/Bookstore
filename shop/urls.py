from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r"categories", CategoriesViewSet, basename="categories")
router.register(r"books", BooksViewSet, basename="books")
router.register(r"payments", PayMethodsViewSet, basename="payments")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"book2cart", BooktoCartViewSet, basename="book2cart")
router.register(r"orders", OrdersViewSet, basename="orders")
router.register(r"addresses", AddressesViewSet, basename="addresses")


urlpatterns=[
] + router.urls
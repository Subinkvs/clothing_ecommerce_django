from django.urls import path
from .import views



urlpatterns = [
    path('',views.home, name="index"),
    path('product/<int:product_id>', views.productdetail, name = "productdetail"),
    path('category/tshirt/', views.tshrit_category, name='tshirt_category'),
    path('category/shirt/', views.shrit_category, name='shirt_category'),
    path('category/jeans/', views.jeans_category, name='jeans_category'),
    path('category/jacket/', views.jacket_category, name='jacket_category'),
    path('add-to-cart', views.addtocart, name="addtocart"),
    path('cart', views.cart, name='cart' ),
    path('update-cart', views.updatecart, name='updatecart'),
    path('delete-cart-item', views.deletecartitem, name='deletecartitem'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('add-to-wishlist', views.addtowishlist, name='addtowishlist'),
    path('delete-wishlist-item', views.deletewishlistitem, name='deletewishlistitem'),
    path('checkoutpage', views.checkoutpage, name='checkoutpage'), 
    path('ordercomplete', views.ordercomplete, name='ordercomplete')

]

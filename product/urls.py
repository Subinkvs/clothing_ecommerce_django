from django.urls import path
from .import views



urlpatterns = [
    path('',views.home, name="index"),
    path('product/<int:product_id>', views.productdetail, name = "productdetail"),
    path('category/tshirt/', views.tshrit_category, name='tshirt_category'),
    path('category/shirt/', views.shrit_category, name='shirt_category'),
    path('category/jeans/', views.jeans_category, name='jeans_category'),
    path('category/jacket/', views.jacket_category, name='jacket_category')
]

from django.urls import path
from .import views



urlpatterns = [
    path('',views.home, name="index"),
    path('product/<int:product_id>', views.productdetail, name = "productdetail"),
    path('allcategories', views.Allcategories, name="allcategories")
]

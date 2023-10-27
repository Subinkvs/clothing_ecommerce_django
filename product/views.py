from django.shortcuts import render, redirect
from .models import  MenClothing, BannerImage,Category
from django.shortcuts import get_object_or_404


# Create your views here.
def home(request):
    prods = MenClothing.objects.filter(is_featured=True)
    bannerimage = BannerImage.objects.all()
    categories = Category.objects.all()
    category_product_mapping = {}
    for category in categories:
        prods = MenClothing.objects.all()
        category_product_mapping[category] = prods
    return render(request, 'index.html', {'prods':prods ,'bannerimage':bannerimage, 'category_product_mapping':category_product_mapping})

def productdetail(request, product_id):
    product = get_object_or_404(MenClothing, pk=product_id)
    return render(request, 'product-detail.html',{'product':product})

def tshrit_category(request):
    tshirts = MenClothing.objects.filter(category__name = 'T-shirt',is_featured=True)
    return render(request, 'category.html', {'category': 'T-shirt', 'products':tshirts})

def shrit_category(request):
    shirts = MenClothing.objects.filter(category__name = 'Shirt',is_featured=True)
    return render(request, 'category.html', {'category': 'shirt', 'products':shirts})

def jeans_category(request):
    jeans = MenClothing.objects.filter(category__name = 'Jeans',is_featured=True)
    return render(request, 'category.html', {'category': 'jeans', 'products':jeans})

def jacket_category(request):
    jackets = MenClothing.objects.filter(category__name = 'Jacket',is_featured=True)
    return render(request, 'category.html', {'category': 'Jacket', 'products':jackets})
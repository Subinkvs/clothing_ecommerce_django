from django.shortcuts import render, redirect
from .models import  MenClothing, BannerImage,Category
from django.shortcuts import get_object_or_404


# Create your views here.
def home(request):
    prods = MenClothing.objects.all()
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

def Allcategories(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories':categories})
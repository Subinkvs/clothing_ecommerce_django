from django.shortcuts import render, redirect
from .models import  MenClothing, BannerImage,Category,Cart,Wishlist
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here. 
def home(request):
    prods = MenClothing.objects.filter(is_featured=True)
    bannerimage = BannerImage.objects.all()
    categories = Category.objects.all()
    cartitem = Cart.objects.filter(user=request.user.id)
    total_quantity = sum(item.product_qty for item in cartitem)
    return render(request, 'index.html', {'prods':prods ,'bannerimage':bannerimage, 'categories':categories, 'cartitem':cartitem, 'total_quantity':total_quantity})

def productdetail(request, product_id):
    product = get_object_or_404(MenClothing, pk=product_id)
    cartitem = Cart.objects.filter(user=request.user)
    total_quantity = sum(item.product_qty for item in cartitem)
    return render(request, 'product-detail.html',{'product':product, 'cartitem':cartitem, 'total_quantity':total_quantity})

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



# def categories(request):
#     categories = Category.objects.all()
#     category_items = {}
#     for cat in categories:
#         item = MenClothing.objects.filter(category__name = cat.name, is_featured = True)
#         category_items[cat.name] = item
        
#     return render(request, 'category.html',{'categories': categories, 'category_items': category_items})


def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = MenClothing.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status':'Product Already in Cart'})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status':'Product added successfully'})
                    else:
                        return JsonResponse({'status':"Only" + str(product_check.quantity) + "quantity avaliable"})
            else:
                return JsonResponse({'status':'No such product found'})
        else:
            return JsonResponse({'status': 'Login to Continue'})
    return redirect('/')

@login_required(login_url='loginpage')
def cart(request):
    cartitem = Cart.objects.filter(user=request.user.id)
    total_quantity = sum(item.product_qty for item in cartitem)
    context = {'cartitem':cartitem, 'total_quantity':total_quantity}
    return render(request, 'cart.html', context)

def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id') )
        if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user.id)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':'Updated Successfully'})
    return redirect('index')

def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
        return JsonResponse({'status':'Deleted Successfully'})
    return redirect('index')


@login_required(login_url='loginpage')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request, 'wishlist.html', context)

def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = MenClothing.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':'Product already in wishlist'})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status':'Product added to wishlist'})
            else:
                return JsonResponse({'status':'No such product found'})
        else:
            return JsonResponse({'status':'Login to continue'})
    return redirect('index')


def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Wishlist.objects.get(product_id=prod_id)
                wishlistitem.delete()
                return JsonResponse({'status':'Product removed from wishlist'})
            else:
                return JsonResponse({'status':'Product not found in wishlist'})
        else:
            return JsonResponse({'status':'Login to continue'})
        
    return redirect('index')
    

def checkoutpage(request):
    rawcart = Cart.objects.filter(user=request.user)
    total_quantity = sum(item.product_qty for item in rawcart)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)
            
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.price * item.product_qty
    
    context = {'cartitems':cartitems, 'total_price':total_price, 'total_quantity':total_quantity}
    return render(request, 'place-order.html', context)        


def ordercomplete(request):
    return render(request, 'order_complete.html')
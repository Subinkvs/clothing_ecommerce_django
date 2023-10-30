from .decorator import user_not_authenticated
from .forms import UserCreationForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from accounts.forms import  CustomUserForm
from django.contrib import messages
from django.contrib.auth import  authenticate, login, logout, get_user_model
from product.models import MenClothing,BannerImage,Category
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import token_generator
from product.models import BannerImage
 
# Create your views here.
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('loginpage')
    else:
        messages.error(request, 'Activation link is invalid')
    
    return redirect('index')
        
def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user':user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user},please go to your email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note:Check your spam folder.')
    else:
        messages.success(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def home(request):
    prods = MenClothing.objects.filter(is_featured=True)
    bannerimage = BannerImage.objects.all()
    categories = Category.objects.all()
    category_product_mapping = {}
    for category in categories:
        prods = MenClothing.objects.filter(is_featured=True)
        category_product_mapping[category] = prods
    return render(request, 'index.html', {'prods':prods ,'bannerimage':bannerimage, 'category_product_mapping':category_product_mapping})

    
@user_not_authenticated
def signuppage(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
           
            return redirect('index')
    context = {'form':form}
    return render(request, 'register.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('/')
    else:
        if request.method == "POST":
           
            name = request.POST.get('username')
            passwd = request.POST.get('password')
            
            user = authenticate(request,username=name,password=passwd, )
            
            if user is not None:
                
                login(request, user)
                messages.success(request, "Logged in Successfully")
                prods = MenClothing.objects.all()
                bannerimage = BannerImage.objects.all()
                return render(request, 'index.html',{'prods':prods, 'bannerimage':bannerimage})
                
               
            else:
                    messages.error(request, "Invalid Username or Password")
                    return redirect('loginpage')
        return render(request, 'signin.html')
    
def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout Successfully")
    return redirect('/')






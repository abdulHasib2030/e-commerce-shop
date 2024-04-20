from django.shortcuts import render
from account.forms import UserRegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from product.models import *
from category.models import Category
from cart.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# from cart.views import _cart_id

def _cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart
# Create your views here.
def home(request):
  products = Product.objects.all()
  review = ProductReview.objects.all()
  quantity = 0
  if request.user.is_authenticated:
    cart_items = CartItem.objects.filter(user=request.user).exists()
    if cart_items:
      cart_items = CartItem.objects.filter(user = request.user)
      for i in cart_items:
        quantity += i.quantity
  else:
    
    cart_id = _cart_id(request)
    if cart_id == None:
      cart_id  = _cart_id(request)
    try:
      cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
      Cart.objects.create(cart_id=cart_id)
      cart = Cart.objects.get(cart_id = cart_id)
    
    
    print(cart)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    if cart_items:
      for i in cart_items:
        quantity += i.quantity
  categories = Category.objects.all()
  fashion_category = Category.objects.get(category_name = "Fashion")
  gadget_category = Category.objects.get(category_name = "Gadget & Gear")
  sports = Category.objects.get(category_name = "Sports")
  home = Category.objects.get(category_name = "Home & Lifestyle")
  fashion = Product.objects.filter(category= fashion_category)
  gadget = Product.objects.filter(category = gadget_category)
  sports = Product.objects.filter(category = sports)
  home = Product.objects.filter(category = home)
  for i in home:
    print(i.category, "Hello world")
  context = {
    'products':products,
    'quantity': quantity,
    'categories': categories,
    'fashion':fashion,
    'gadget':gadget,
    'review':review,
    'sports':sports,
    'home':home,
  }
  for i in review:
    
    print(i.user_name)
  return render(request, 'home.html', context)

########## User Registration ###########
def UserRegisterView(request):
  quantity = 0
  cart_id = _cart_id(request)
  try:
    cart = Cart.objects.get(cart_id=cart_id)
  except Cart.DoesNotExist:
    Cart.objects.create(cart_id=cart_id)
    cart = Cart.objects.get(cart_id = cart_id)

  cart_items = CartItem.objects.filter(cart=cart, is_active=True)
  
  if cart_items:
    for i in cart_items:
      quantity += i.quantity
      
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      for i in form.errors.values():
        messages.success(request, i)     
  else:
    form = UserRegistrationForm
  context = {
    'form':form,
    'quantity':quantity
  }
  return render(request, 'authenticate/signup.html', context)

    
########### User Login ###############
def UserLoginView(request):
    quantity = 0
    cart_id = _cart_id(request)
   
    if cart_id != None:
      try:
        cart = Cart.objects.get(cart_id=cart_id)
      except Cart.DoesNotExist:
        Cart.objects.create(cart_id=cart_id)
        cart = Cart.objects.get(cart_id = cart_id)

      cart_items = CartItem.objects.filter(cart=cart, is_active=True)
      
      if cart_items:
        for i in cart_items:
          quantity += i.quantity
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        user = authenticate(username= username , password = password)
        print(user)
 
        if user is not None:
            session_id = request.session.session_key
            cart = Cart.objects.get(cart_id=session_id)
            cart_item_exit = CartItem.objects.filter(cart=cart).exists()
            if cart_item_exit:
              cart_item = CartItem.objects.filter(cart=cart)
              cart_item2 = CartItem.objects.filter(user = user)
              for i in cart_item:
                flag = True
                for j in cart_item2:
                  if i.product == j.product:
                    j.quantity += i.quantity
                    j.save()
                    flag = False
                if flag == True:
                  i.user = user
                  i.save()
                    
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'authenticate/login.html', {'quantity':quantity})
   
    
# ########### User Logout ############
@login_required(login_url='login')
def logoutView(request):
  logout(request)
  messages.success(request, 'Your are logged out.')
  return redirect('login')

##### Forgot Password ########

def forgetPassword(request):
  if request.method == 'POST':
    email = request.POST['email']
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email__exact = email)
      #Reset password Email
      current_site = get_current_site(request)
      mail_subject = 'Reset your Password'
      message = render_to_string('authenticate/reset_password_email.html', {
        'user': user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
      })
      to_email = email
      send_email = EmailMessage(mail_subject, message, to=[to_email])
      send_email.send()
      
      messages.success(request, 'Password reset email has been sent to your email address.')
      return redirect('login')
    else:
      messages.success(request, 'Account does not exist!')
      return redirect('forgotPassword')
  return render(request, 'authenticate/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  if user is not None and default_token_generator.check_token(user, token):
    request.session['uid'] = uid
    messages.success(request, 'Please reset your password')
    return redirect('resetPassword')
  else:
    messages.error(request, "This link has been expired!")
    return redirect('login')

def resetPassword(request):
  if request.method == 'POST':
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    if password == confirm_password:
      uid = request.session.get('uid')
      user = User.objects.get(pk = uid)
      user.set_password(password)
      user.save()
      messages.success(request, 'Password reset successful')
      return redirect('login')
    else:
      messages.error(request, "Password do not match!")
      return redirect('resetPassword')
  else:
    return render(request, 'authenticate/resetPassword.html')

@login_required(login_url='login')
def profileInfo(request):
  quantity = 0
  cart_items = CartItem.objects.filter(user=request.user).exists()
  if cart_items:
    cart_items = CartItem.objects.filter(user = request.user)
    for i in cart_items:
      quantity += i.quantity
 
  bill = BillingDetails.objects.filter(user = request.user)
  order = Order.objects.filter(user = request.user)
  for i in bill:
    for j in i.product.all():
      print(j.images)
  
  context = {
    'bill':bill,
    'order':order,
    'quantity':quantity,
  }
  
    

  return render(request, 'profile.html', context)
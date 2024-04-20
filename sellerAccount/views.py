from django.shortcuts import render, redirect, HttpResponse
from sellerAccount.models import sellerAccount
from sellerAccount.forms import *
from django.core.mail import send_mail
import random
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from category.models import Category
from product.models import Product, Size
from cart.models import *
from cart.views import _cart_id

# Create your views here.
def sellerAccountView(request):
  products = Product.objects.all()
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
  if request.method == 'POST':
    form = sellerAccountForm(request.POST)
    # print(form)
    if form.is_valid():
      email = (form.cleaned_data['email'])
      business_name =form.cleaned_data['business_name']
      owner_name = form.cleaned_data['owner_name']
      link = 'http://127.0.0.1:8000/seller/active/'
      
      uid = urlsafe_base64_encode(force_bytes(business_name))
      # token = default_token_generator.make_token(owner_name)
      print(uid)
      
      
      otp = 1234
      mess = f'''Hello {owner_name} 
Your Seller Account Confirm Link {link}{uid}
  
  
Your Business name: {business_name}
      '''
      sub = f'Confirm your Seller Account Business Name: {business_name}'
      sender = 'abdulhasib2030@gmail.com'
      lst = []
      lst.append(email)
      
      send_mail(sub, mess, sender, lst)
      form.save()
      # return redirect('active', uid)
      messages.success(request, 'Check your Email and Confirm Your Seller Account.')
  else:
    form = sellerAccountForm()
  context = {
    'form':form,
    'quantity':quantity,
  }
  return render(request, 'signup.html', context)

def confirmEmail(request, uid):
  if request.method == 'POST':
    Uid= uid
    idd = smart_str(urlsafe_base64_decode(Uid))
    # print(id)
    seller = sellerAccount.objects.get(business_name=idd)
    if seller:
      seller.is_active = True
      seller.save()
      return redirect('dashboard', seller.slug)
  return render(request, 'active.html')


  
def sellerLogin(request):
  products = Product.objects.all()
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
  if request.method == 'POST':
    business_number = request.POST['business_number']
    password = request.POST['password']
    try:
      seller_user = sellerAccount.objects.get(phone = business_number, password = password, is_active = True)
      return redirect('dashboard', seller_user.slug)
      # return render(request, 'base_dashboard.html', {'seller_user':seller_user})
    except sellerAccount.DoesNotExist:
      messages.success(request, "Invalid login credentials ")
      return redirect('seller_login')
    # if user:
    #   return HttpResponse("Successfully Seller Login")
    # else:
    #   return HttpResponse("Information Invalid.")
  
  return render(request, 'login.html', {'quantity':quantity})      

def sellerDashboard(request, owner_name):
  print(owner_name)
  order = BillingDetails.objects.filter(product__seller_account__slug = owner_name)
  lst = []
  qu = []
  for i in order:
    tem = i.quantity.split()
    lst.append((i.product.filter(seller_account__slug = owner_name)))
    for j in i.product.filter(seller_account__slug = owner_name):
      ll = 0
      for k in i.product.all():
        if k.product_name == j.product_name:
          qu.append(tem[ll])
        ll += 1
  tem1 = []
  tem2 = []
  for i in lst:
    for j, k in zip(i, qu):
      tem1.append(j)
      tem2.append(k)
  seller = sellerAccount.objects.get(slug = owner_name)
  # for i in lst:
  #   for j in i:
  #     print(j.price)
  #   print()
  tem3 = zip(tem1, tem2)
  print(tem3)
  context = {
    'seller_user': seller,
    'order':order,
    'lst':lst,
    'qu':qu,
    'lstt': tem3,
  }
  return render(request, 'dashboard/order_lst.html', context)

def categoryShow(request, owner_name):
  print(id, "HEllo world")
  category = Category.objects.all()
  lst = {}
  # print(sellerAccount.objects.get(id= request.id))
  seller = sellerAccount.objects.get(slug = owner_name)
  for i in category:
    product = Product.objects.filter(category=i, seller_account= seller)
    print(product)
    lst[i.category_name] = len(product) 
  
  context = {
    'category': category,
    'len': len(category),
    'lst':lst,
    'seller_user':seller,
    
  }
  return render(request, 'dashboard/category.html', context)

def productList(request, owner_name):
  print(owner_name)
  seller = sellerAccount.objects.get(slug = owner_name)
  product = Product.objects.filter(seller_account=seller)
  dic = {}
  for i in product:
    
    sum = 0
    for j in i.size.all():
      sum += (j.quantity)
    dic[i.product_name] = sum
    dic[i.category] = sum
    print(sum)
  context = {
    'seller_user': seller,
    'products':product,
  }
  return render(request, 'dashboard/product_list.html', context)

def addProduct(request, owner_name):
  seller = sellerAccount.objects.get(slug = owner_name)
  category = Category.objects.all()
  if request.method == 'POST':
    try:
      product_name = request.POST['product_name']
      description = request.POST['description']
      price = request.POST['price']
      
      images = request.POST['images']
      quantity = request.POST['quantity']
      category_ = request.POST['category']
      category_ = Category.objects.get(category_name = category_)
      size = request.POST['size']
      size0, size1= 0, 0
      quantity0, quantity1 = 0, 0
      try:
        size0 = request.POST['size0']
        size1 = request.POST['size1']
        quantity0 = request.POST['quantity0']
        quantity1 = request.POST['quantity1']
      except Exception as e:
        pass
      
      discount_price = request.POST['discount_price']
      lst = []
      sub = Size.objects.create(size=size, quantity = quantity)
      lst.append(sub.id)
      if size0 != 0:
        sub = Size.objects.create(size= size0, quantity = quantity0)
        lst.append(sub.id)
      if size1 != 0:
        sub = Size.objects.create(size = size1, quantity = quantity1)
        lst.append(sub.id)
      print(images)
      
      sizeAd = Size.objects.filter(id__in = lst)
      sum = 0
      for i in sizeAd:
        sum += i.quantity
      product = Product.objects.create(seller_account= seller, product_name=product_name, description=description, price=price, images=images,stock=sum, category=category_,  discount_price=discount_price)
      product.size.set(sizeAd)
      product.save()
      
      return redirect('seller_info', owner_name)
    except Exception as e:
      messages.success(request, f'Wrong Information Provide.')
    # print(product_name, size, size0, size1, category_)
  context = {
     'categorys':category,
    'seller_user': seller,
  }
  return render(request, 'dashboard/add_product.html', context)

def orderList(request, owner_name ):
  seller = sellerAccount.objects.get(slug = owner_name)

  order = BillingDetails.objects.all()
  for i in order:
    print(i.first_name)
  context = {
    'seller_user':seller,
  }
  return render(request, "dashboard/order_lst.html", context)

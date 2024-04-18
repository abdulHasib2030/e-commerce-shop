from django.shortcuts import render, get_object_or_404, redirect
from product.models import *
from category.models import Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from cart.views import _cart_id
from cart.models import *
from django.contrib import messages

# Create your views here.
def store(request, id = None, price = None):
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
  products= None
  categories = None
  print(id, price)
  if id:
        category = get_object_or_404(Category, id = id)
        print(category)
        products = Product.objects.filter(
            is_available=True, category=category)  # category wise products
        page = request.GET.get('page')
        print(page)
        
        paginator = Paginator(products, 3)
        paged_product = paginator.get_page(page)
  else:
      products = Product.objects.filter(is_available=True)  # all products
      # Paginator(objects, per page e kotogula product dekhte chai)
      paginator = Paginator(products, 3)
      page = request.GET.get('page')
      paged_product = paginator.get_page(page)
      # print(paged_product)
      # for i in paged_product:
      #     print(i)
      # print(paged_product.has_next(), paged_product.has_previous(),
      #       paged_product.previous_page_number, paged_product.next_page_number)
 
  if price:
        # category = get_object_or_404(Category, id = id)
        products = Product.objects.filter(
            is_available=True, price__range=(0, price))  # category wise products
        page = request.GET.get('page')
        print(page)
        # Paginator(objects, per page e kotogula product dekhte chai)
        paginator = Paginator(products, 3)
        paged_product = paginator.get_page(page)
  

  ### Prize Sorting
  if 'min_price' in request.GET:    
        filter_price1 = request.GET.get('min_price')
        filter_price2 = request.GET.get('max_price')
        if filter_price1 =='':
            filter_price1=0
        paged_product = Product.objects.filter(price__range=(filter_price1,filter_price2))
        
  categories = Category.objects.all()
  context = {
      'products': paged_product, 
      'categories': categories, 
      'quantity':quantity,
      }
  return render(request, 'store.html', context)

  

def Product_detail(request, category_slug, product_slug):
  quantity = 0
  cart_id = _cart_id(request)
  if request.user.is_authenticated:
    cart_items = CartItem.objects.filter(user=request.user).exists()
    if cart_items:
      cart_items = CartItem.objects.filter(user = request.user)
      for i in cart_items:
        quantity += i.quantity
  else:
    
    cart_id = _cart_id(request)
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
  try:
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    cart_items = None
    cart_items = CartItem.objects.get( cart=cart)
  except Exception as e:
    messages.success(request, "error")
  print(quantity)
  products = Product.objects.filter(category = single_product.category)
  print(cart_items, "Hellow lkajkasf")
  categories = Category.objects.all()
  try: 
    if request.method == 'POST':
    
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        rating = request.POST['rating']
        
        ProductReview.objects.create(user=request.user, product= single_product, user_name = name, email = email, review = message, rating=rating)
        messages.success(request, "Successfully Rating add this product.")
  except:
    messages.error(request, "Error")
  rating = ProductReview.objects.all()
  context = {
    'rating':rating,
    'single_product':single_product,
    'quantity':quantity,
    'cart_item':cart_items,
    'products':products,
    'categories':categories,
  }
  
  
  return render(request, 'product_details.html', context)

def search(request):
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
  
 
  if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if keyword:
      products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains = keyword))
      product_count = products.count()
      
      # Paginator(objects, per page e kotogula product dekhte chai)
      paginator = Paginator(products, 3)
      page = request.GET.get('page')
      paged_product = paginator.get_page(page)
    else:
      # messages.success(request, "Type your need.")
      return redirect('store')
  
  categories = Category.objects.all()
  context = {
    'products':paged_product,
    'p_count':product_count,
    'quantity':quantity,
    'categories':categories,
  }
  return render(request, 'store.html', context)


def ProductRationView(request):
  if request.method == 'POST':
   
      name = request.POST['name']
      email = request.POST['email']
      message = request.POST['message']
      rating = request.POST['rating']
      print(name, email, message, rating, product_id)
      ProductReview.objects.create(user=request.user, product= product_id, user_name = name, email = email, review = message, rating=rating)
      
    
  return render(request, 'product_details.html')
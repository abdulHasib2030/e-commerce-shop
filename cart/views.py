from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from cart.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random

# Create your views here.
def _cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # Get the product
    print(product)
    
    # cart_itm = CartItem.objects.get(product=product)
    # If the user is authenticated
    if current_user.is_authenticated:
        # Check if the cart item already exists for this product and user
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        print(product)
        print(request.session)
        if is_cart_item_exists:
            
            # Use .get() with filter parameters to retrieve the specific cart item
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            # item = CartItem.objects.get(product=product, user=current_user)
            
            item = CartItem.objects.get(product=product, user=current_user)
            
            
            item.quantity += 1
            item.save()
            # item.quantity += 1
            # item.save()
            print("yes")
            
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
                user = current_user
            )
            cart_item.save()
        messages.success(request, 'Successfully added cart item.')
        return redirect('home')
    else:
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity  += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                )
            cart.save()
    messages.success(request, 'Successfully added cart item.')
    return redirect('home')
  
def add_cart_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # Get the product
    # cart_itm = CartItem.objects.get(product=product)
    # If the user is authenticated
    if current_user.is_authenticated:
        # Check if the cart item already exists for this product and user
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_item_exists:  
            # Use .get() with filter parameters to retrieve the specific cart item
            # cart_items = CartItem.objects.filter(product=product, user=current_user)
            # item = CartItem.objects.get(product=product, user=current_user)
            
            item = CartItem.objects.get(product=product, user=current_user)
       
            item.quantity += 1
            item.save()
            
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
                user = current_user
            )
            cart_item.save()
        messages.success(request, 'Successfully added cart item.')
        return redirect('cart')
    else:
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity  += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                )
            cart.save()
    messages.success(request, 'Successfully added cart item.')
    return redirect('cart')



def cart(request, total=0, quantity = 0, cart_items = None):
  try:
    shipping = 100
    grand_total = 0
    coupon = 0
  
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_items = CartItem.objects.filter(cart=cart, is_active=True)
          
    for cart_item in cart_items:
      # print(cart_item.product)
      total += (cart_item.product.main_price() * cart_item.quantity)
      quantity += cart_item.quantity
    if total >= 2000:
      shipping = "Free Delivery"
      grand_total = total
    else:
      grand_total = total + shipping
  except ObjectDoesNotExist:
    pass
  
  if request.method == 'POST':
    coupon_name = request.POST['coupon_name']
    
    if request.user.is_authenticated:
      coupon_name = coupon_name.lower()
      print(coupon_name)
      try:
        FirstOrderCoupon.objects.get(user = request.user)
        messages.success(request, "This voucher does not exist for you.")
      except FirstOrderCoupon.DoesNotExist:
        if coupon_name == 'firstorder':
          
          coupon = (total * 20) / 100
          messages.success(request, 'Successfully Applied Coupon')
        else:
          messages.success(request, "This voucher does not exist. Please check if the voucher code was keyed in correctly.") 
  
  if coupon > 100:
    coupon = 100
  context = {
    'total':total,
    'quantity':quantity,
    'cart_items':cart_items,
    'shipping': shipping,
    'coupon':coupon,
    'grand_total':grand_total-coupon,
  }
  return render(request, 'cart.html', context)
  # return render(request, 'cart.html')

def remove_cart(request, product_id, cart_item_id):
  product = get_object_or_404(Product, id=product_id)
  try:
    if request.user.is_authenticated:   
      cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id)
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    
    if cart_item.quantity > 1:
      cart_item.quantity -= 1
      cart_item.save()
    else:
      cart_item.delete()
  except:
    pass
  return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
  product = get_object_or_404(Product, id = product_id)
  if request.user.is_authenticated:
    cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
  else:
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(cart=cart, product=product, id = cart_item_id)
  
  cart_item.delete()
  return redirect('cart')

##### Checkout Page ####
@login_required(login_url='login')
def checkOutView(request, coupon):
  shipping = 100
  cart_item = CartItem.objects.filter(user=request.user)
  if request.method == 'POST':
    first_name = (request.POST['first_name'])
    last_name = request.POST['last_name']
    address = request.POST['address']
    town_city = request.POST['town_city']
    country = request.POST['country']
    zipcode = request.POST['zip_code']
    mobile = request.POST['mobile']
    email_address = request.POST['email_address']
    note = request.POST['text']
    
    
    if first_name == "" or last_name == "" or address == "" or town_city == "" or country == "" or len(str(zipcode)) < 1 or len(str(mobile))  > 11 or len(str(mobile)) < 11 or str(email_address).find('@') == -1:
      messages.success(request, "You not provided all information in billing.")
      return redirect('checkout')
    else:
      
      bill = BillingDetails.objects.create(first_name=first_name, last_name=last_name, address = address, town_city=town_city, country=country, zipcode=zipcode, mobile = mobile, email_address = email_address, note = note)
      quantity = ""
      total = 0
      for i in cart_item:
        total += i.product.main_price() * i.quantity
        i.product.stock -= i.quantity
        i.product.save()
        bill.product.add(i.product)
        quantity += str(i.quantity)
        quantity += " "
      print(total)
      bill.sub_total = total
      bill.quantity = quantity
      bill.user = request.user
      bill.save()
      
      if coupon:
        FirstOrderCoupon.objects.create(user = request.user, available = True)
      cart_item.delete()
      order_id = "thaj"
      order_id += str(request.user.id) + str(random.randint(1,1000))
      try:
        Order.objects.get(order_id = order_id)
        Order.objects.create(order_id = order_id + str(random.randint(1,1000), user = request.user))
      except:
        Order.objects.create(order_id = order_id, user = request.user)

      
      return render(request, 'order_success.html')
  total, subtotal = 0, 0
  for i in cart_item:
    total += i.quantity * i.product.main_price()
  if total >= 2000:
    shipping = 'Free Delivery'
    subtotal = total 
  else:
    subtotal = total + 100
  context = {
    'cart_items':cart_item,
    'total': total,
    'shipping':shipping,
    'quantity':0,
    'coupon':coupon,
    'subtotal':subtotal-coupon,
  }
  return render(request, 'checkout.html', context)

def add_product_detail_cart(request, product_id):
  add_cart_cart(request, product_id)
  product= Product.objects.get(id = product_id)
  
  return redirect('product_detail', product.category.slug, product.slug)

def remove_product_detail_cart(request, product_id, cart_item_id):
  remove_cart(request, product_id, cart_item_id)
  product = Product.objects.get(id = product_id)
  
  return redirect('product_detail', product.category.slug, product.slug)

def store_cart(request, product_id):
  add_cart(request, product_id)
  return redirect('store')



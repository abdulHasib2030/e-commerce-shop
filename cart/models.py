from django.db import models
from product.models import Product
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Cart(models.Model):
  cart_id = models.CharField(max_length=250, blank=True)
  date_added = models.DateField(auto_now_add=True)
  
  def __str__(self):
      return self.cart_id

class CartItem(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
  product = models.ForeignKey(Product, on_delete= models.CASCADE)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
  quantity = models.IntegerField()
  is_active = models.BooleanField(default=True)
  
  def sub_total(self):
    return self.product.main_price() * self.quantity
  def get_url(self):
    return reverse('remove_cart', args=[self.product.id, self.id])
  
  
  # def __str__(self):
  #     return self.product
  
class BillingDetails(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  town_city = models.CharField(max_length=100)
  country = models.CharField(max_length=100)
  zipcode = models.IntegerField()
  mobile = models.IntegerField()
  email_address = models.EmailField()
  note = models.TextField(max_length=500)
  product = models.ManyToManyField(Product, null=True, related_name= "products")
  quantity = models.CharField(max_length = 200, null=True)
  user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
  def sub_total(self):
    return self.product.price * self.quantity
  
class FirstOrderCoupon(models.Model):
  user = models.OneToOneField(User, on_delete= models.CASCADE)
  available = models.BooleanField(default= False)

class Order(models.Model):
  order_id = models.CharField(max_length= 20)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

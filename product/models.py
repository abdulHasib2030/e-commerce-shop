from django.db import models
from category.models import Category
from sellerAccount.models import sellerAccount
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
SIZE = (
  ('M', 'M'),
  ('L', 'L'),
  ('XL', 'XL'),
)
    
class Size(models.Model):
  size = models.CharField(max_length=200, choices= SIZE)
  quantity = models.IntegerField()
    
  
class Product(models.Model):
  seller_account = models.ForeignKey(sellerAccount, on_delete=models.CASCADE, null=True)
  product_name = models.CharField(max_length=2000,  unique=True)
  slug = models.SlugField(max_length= 2500, unique=True)
  description = models.TextField(max_length= 10000, blank=True)
  price = models.IntegerField()
  images = models.FileField()
  stock = models.IntegerField(null= True)
  is_available = models.BooleanField(default=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add= True)
  modified_date = models.DateTimeField(auto_now= True)
  discount_price = models.IntegerField(null=True) 
  size = models.ManyToManyField(Size,  null=True)
  
  def __str__(self):
      return self.product_name
  
  def main_price(self):
    if self.discount_price > self.price:
      return 0
    return self.price - self.discount_price
  
  def get_url(self):
    return reverse('product_detail', args = [self.category.slug, self.slug])
  
  
  
  # def get_sigle_url(self):
  #   return reverse('remove_cart', args= [self.cate])
  
  def save(self, *args, **kwargs):
    self.slug = slugify(self.product_name)
    super(Product, self).save(*args, **kwargs)

class ProductReview(models.Model):
  user = models.ForeignKey(User, on_delete= models.CASCADE)
  product = models.ForeignKey(Product, on_delete= models.CASCADE)
  user_name = models.CharField(max_length= 300)
  email = models.EmailField()
  review = models.TextField(10000)
  rating = models.IntegerField()
  created_at = models.DateField(auto_now_add=True, null=True)
  
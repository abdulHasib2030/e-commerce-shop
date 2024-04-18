from django.db import models
import secrets
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.
class sellerAccount(models.Model):
  business_name = models.CharField(max_length= 255)
  owner_name = models.CharField(max_length= 250)
  slug = models.SlugField(max_length= 280, null=True)
  phone = models.IntegerField(unique=True)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length= 50)
  city = models.CharField(max_length= 200)
  area = models.CharField(max_length= 200)
  zone = models.CharField(max_length= 200)
  address = models.TextField(max_length= 500)
  nid = models.IntegerField()
  is_active = models.BooleanField(default=False)
  
  def get_url(self):
    return reverse('seller_info', args=[self.slug])
  def get_url_categroy(self):
    return reverse('category_list', args=[self.slug])
  def get_url_addProduct(self):
    return reverse('add_product', args = [self.slug])
  def save(self, *args, **kwargs):
    self.slug = slugify(self.owner_name)
    super(sellerAccount, self).save(*args, **kwargs)
  
class otpToken(models.Model):
  user = models.ForeignKey(sellerAccount, on_delete= models.CASCADE)
  otp_code = models.CharField(max_length=10, default=secrets.token_hex(3))
  tp_created_at = models.DateTimeField(auto_now_add= True)
  otp_expires_at = models.DateTimeField(blank=True, null= True)
  
  

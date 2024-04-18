from django import forms
from sellerAccount.models import sellerAccount
from product.models import Product

class sellerAccountForm(forms.ModelForm):
  class Meta:
    model = sellerAccount
    fields = ['business_name', 'owner_name', 'phone', 'email', 'password', 'city', 'area', 'zone', 'address', 'nid']
    
    widgets = {'password':forms.PasswordInput()}
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields:
      self.fields[field].widget.attrs.update({
            'class': (
                'form-control'
            )})
      if field == 'business_name':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter Business Name'
            )})
      elif field == 'owner_name':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter Owner Name'
            )})
      elif field == 'phone':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter Phone Number'
            )})
      elif field == 'email':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter Email'
            )})
      elif field == 'password':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter Password'
            )})
      elif field == 'city':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter City'
            )})
      elif field == 'area':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter Area'
            )})
      elif field == 'zone':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter Zone'
            )})
      elif field == 'address':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter Address'
            )})
      elif field == 'nid':
        self.fields[field].widget.attrs.update({
            'placeholder': (
                'Enter NID Number'
            )})
  
class addProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'images', 'stock', 'category']




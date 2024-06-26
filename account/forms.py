from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

###### User Registration Form #####
class UserRegistrationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2', 'email']
    
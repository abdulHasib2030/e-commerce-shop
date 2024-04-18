from django.urls import path
from account.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name= 'home'),
    path('signup/', UserRegisterView, name= "signup"),
    path('login/', UserLoginView, name= "login"),
    path('forgotPassword/', forgetPassword, name='forgotPassword'),
     path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name='resetpassword_validate'),
    
    path('resetPassword/', resetPassword, name='resetPassword'),
    path('logout/', logoutView, name = 'logout'),
    
    path('profile/', profileInfo, name='profile'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

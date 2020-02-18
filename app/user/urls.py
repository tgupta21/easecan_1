from django.urls import path

from . import views
from knox import views as knox_views

app_name = 'user'

urlpatterns = [
    path('signup/', views.MerchantSignupView.as_view(), name='create'),
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logout_all/', knox_views.LogoutAllView.as_view(), name='knox_logout_all'),
]

from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.MerchantSignupView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
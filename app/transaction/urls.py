from django.urls import path

from . import views

app_name = 'transaction'

urlpatterns = [
    path('initiate/', views.InitiatePayment.as_view(), name='initiate'),
]

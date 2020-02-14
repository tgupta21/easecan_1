from django.urls import path

from . import views

app_name = 'transaction'

urlpatterns = [
    path('payment/initiate/', views.InitiatePaymentView.as_view(), name='initiate'),
    path('payment/success/', views.PaymentCompletionView.as_view(), name='success'),
]

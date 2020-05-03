from django.urls import path

from . import views

app_name = 'transaction'

urlpatterns = [
    path('payment_request/', views.PaymentRequestView.as_view(), name='payment_request'),
    path('currency_converter/', views.CurrencyConverterView.as_view(), name='currency_converter'),
    path('initiate_payment/', views.InitiatePaymentView.as_view(), name='initiate_payment'),
    path('complete_payment/', views.CompletePaymentView.as_view(), name='complete_payment'),
]

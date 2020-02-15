from django.urls import path

from . import views

app_name = 'transaction'

urlpatterns = [
    path('payment_request/', views.PaymentRequestView.as_view(), name='request'),
    path('initiate_payment/', views.InitiatePaymentView.as_view(), name='initiate'),
    path('complete_payment/', views.CompletePaymentView.as_view(), name='complete')
]

from django.urls import path

from . import views

app_name = 'transaction'

urlpatterns = [
    path('payment_request/', views.PaymentRequestView.as_view(), name='request'),
]

from django.urls import path
from . import views

app_name = 'authorisation'

urlpatterns = [
    path('token/', views.AuthTokenView.as_view(), name='generate'),
]

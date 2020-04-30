from django.urls import path

from . import views

app_name = 'transaction'

urlpatterns = [
    path('create_category/', views.CreateCategory.as_view(), name='NewCategory'),
]

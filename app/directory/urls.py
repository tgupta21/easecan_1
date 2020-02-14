from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('static', views.StaticDirectoryViewSet)

app_name = 'directory'

urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework import serializers
from .models import Category , AnyAmountObject, FetchAmountObject, FixedAmountObject


class CategorySerializer(serializers.ModelSerializer):
    """Serializer to creating a new category in quick payments"""
    class Meta:
        model = Category
        fields = ('name', 'type', 'fetch_url', 'fetch_headers', 'confirmation_url', 'confirmation_headers')
from rest_framework import serializers
from .models import Directory


class CreateStaticDirectory(serializers.ModelSerializer):
    """Generate Static(no amount) Directory"""
    class Meta:
        model = Directory
        fields = ('uid', 'display_name')
        read_only_field = ('uid', )

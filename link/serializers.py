# link/serializers.py
from rest_framework import serializers
from .models import Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'  # Укажите нужные поля
        depth = 1 
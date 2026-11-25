from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'type', 'location', 'status', 'created_at']

    # Кастомная валидация (для 422 кода)
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Заголовок должен быть длиннее 5 символов.")
        return value
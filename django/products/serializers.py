from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):

    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'handle', 'price']

    name = serializers.CharField()
    handle = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.handle = validated_data.get('handle', instance.handle)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

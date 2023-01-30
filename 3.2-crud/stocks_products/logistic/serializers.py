import requests
from rest_framework import serializers
from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'quantity', 'product', 'stock', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        # # создаем склад по его параметрам
        stock = Stock.objects.create(**validated_data)
        StockProduct.objects.create(stock_id=stock, **positions)
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return instance

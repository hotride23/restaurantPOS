from rest_framework import serializers

from .models.category import Category
from .models.order import Order
from .models.order_item import OrderItem
from .models.product import Product
from .models.table import Table


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class CookerOrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'order', 'start_time', 'count', 'is_ready']
        read_only_fields = ['id', 'product', 'order', 'start_time', 'count']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer

    class Meta:
        model = OrderItem
        fields = '__all__'
        total_cost = serializers.ReadOnlyField()


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    table = TableSerializer
    order_item = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        data = validated_data.pop('order_item')
        order = Order.objects.create(**validated_data)
        for order_item_data in data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order

    def update(self, validated_data, **kwargs):
        data = validated_data.pop('order_item')
        order = Order.objects.create(**validated_data)
        for order_item_data in data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order


class WaiterOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    order = OrderSerializer

    class Meta:
        model = OrderItem
        fields = '__all__'

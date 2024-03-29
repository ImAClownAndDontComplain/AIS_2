from rest_framework import serializers
from .models import Product, Customer
from datetime import datetime

TYPES = [
        ('SberPay', 'SberPay'),
        ('GooglePay', 'GooglePay'),
        ('Card', 'Card'),
        ('QR-code', 'QR-code'),
    ]

class CustomerSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=20)
    email = serializers.EmailField()


class ProductSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=100)
    quantity_in_stock = serializers.IntegerField()
    prime_cost = serializers.DecimalField(max_digits=5, decimal_places=2)
    final_cost = serializers.DecimalField(max_digits=5, decimal_places=2)


class OrderWithProductsSerializer(serializers.Serializer):
    products = Product.objects.all()
    PRODUCTS = []
    for product in products:
        PRODUCTS.append(product.product_name)

    customer = serializers.CharField(max_length=20)
    
    products = serializers.ListField(
        child=serializers.ChoiceField(choices=PRODUCTS)
    )
    date_time = serializers.DateTimeField()
    payment_type = serializers.ChoiceField(choices=TYPES)

class ProductWithCostSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=20)
    product_cost = serializers.DecimalField(max_digits=5, decimal_places=2)

class OrderWithProductsSerializerGET(serializers.Serializer):
    order_id = serializers.IntegerField()
    customer = serializers.CharField(max_length=20)
    order_cost = serializers.DecimalField(max_digits=7, decimal_places=2)
    products = serializers.ListField(
        child=ProductWithCostSerializer()
    )
    date_time = serializers.DateTimeField()
    payment_type = serializers.CharField(max_length=20)


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_cost = serializers.DecimalField(max_digits=7, decimal_places=2)
    date_time = serializers.DateTimeField()


class PaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_type_id = serializers.IntegerField()

class PaymentTypeSerializer(serializers.Serializer):
    payment_type = serializers.CharField(max_length=20)

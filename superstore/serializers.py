from rest_framework import serializers
from .models import *
from datetime import datetime

class OrderDetailsSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all())
    discount = serializers.SerializerMethodField()
    total_after_discount = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetails
        fields = ['product', 'product_name', 'price_at_sale', 'quantity', 'total_price', 'discount', 'total_after_discount']

    def get_discount(self, obj):
        return obj.discount
    
    def get_total_after_discount(self, obj):
        return obj.total_after_discount
    
class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = ['address_id', 'region', 'city', 'state', 'country', 'postal_code']
    
class CustomersSerializer(serializers.ModelSerializer):
    address = AddressesSerializer(read_only=True)
    
    class Meta:
        model = Customers
        fields = ['customer_id', 'customer_first_name', 'customer_last_name', 'customer_segment', 'address']

class OrdersSerializer(serializers.ModelSerializer):
    order_details = OrderDetailsSerializer(many=True)
    customer = serializers.CharField(write_only=True)

    class Meta:
        model = Orders
        fields = ['order_id', 'order_date', 'ship_mode', 'customer', 'order_details']

    def create(self, validated_data):
        order_details_data = validated_data.pop('order_details')
        customer_id = validated_data.pop('customer')
        #Retrieval of Customer instance to create Order instance
        customer = Customers.objects.get(customer_id=customer_id)
        order = Orders.objects.create(customer=customer, **validated_data)
        order.save()
        #Creation of OrderDetails instances for the Order instance
        for order_detail in order_details_data:
            OrderDetails.objects.create(order=order, **order_detail)
        return order

    #Defines how order data is represented when GET request is made
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer'] = CustomersSerializer(instance.customer).data
        return representation

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['product_id', 'product_name', 'product_info', 'product_category', 'product_sub_category', 'product_unit_price']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['ship_date']
    
    def validate_ship_date(self, value):
        if value < datetime.today().date():
            raise serializers.ValidationError("Ship date cannot be before today's date")
        return value
    
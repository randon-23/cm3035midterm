from django.contrib import admin
from .models import *

class AddressesAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'region', 'city', 'state', 'country', 'postal_code')

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'product_info', 'product_category', 'product_sub_category', 'product_unit_price')

class CustomersAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'customer_first_name', 'customer_last_name', 'customer_segment', 'address')

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_date', 'ship_date', 'ship_mode', 'customer')

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order_detail_id', 'order', 'product', 'quantity', 'total_price', 'discount', 'total_after_discount')

admin.site.register(Addresses, AddressesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
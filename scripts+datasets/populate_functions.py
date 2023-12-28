import datetime
from decimal import Decimal
from superstore.models import *

def convert_date_format(date):
    try:
        return datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return None

def create_address(row):
    address = Addresses.objects.create(
        region=row['Region'],
        city=row['City'],
        state=row['State'],
        country=row['Country'],
        postal_code=row['Postal Code']
    )
    address.save()
    return address

def create_product(row):
    product = Products.objects.create(
        product_id=row['Product ID'],
        product_name=row['Product Name'],
        product_info=row['Product Info'],
        product_category=row['Category'],
        product_sub_category=row['Sub-Category'],
        product_unit_price=row['Unit Price']
    )
    product.save()
    return product

def create_customer(row):
    address = Addresses.objects.get(postal_code=row['Postal Code'])
    customer = Customers.objects.create(
        customer_id=row['Customer ID'],
        customer_first_name=row['Customer First Name'],
        customer_last_name=row['Customer Last Name'],
        customer_segment=row['Segment'],
        address=address
    )
    customer.save()
    return customer

def create_order(row):
    customer = Customers.objects.get(customer_id=row['Customer ID'])

    order_date_row = row['Order Date']
    ship_date_row = row['Ship Date']
    
    order = Orders.objects.create(
        order_id=row['Order ID'],
        order_date=convert_date_format(order_date_row),
        ship_date=convert_date_format(ship_date_row),
        ship_mode=row['Ship Mode'],
        customer=customer
    )
    order.save()
    return order

def create_order_detail(row):
    order = Orders.objects.get(order_id=row['Order ID'])
    product = Products.objects.get(product_id=row['Product ID'])
    order_detail = OrderDetails(
        order=order,
        product=product,
        product_name=row['Product Name'],
        price_at_sale=Decimal(row['Unit Price']),
        quantity=int(row['Quantity']),
        discount=Decimal(row['Discount'])
    )
    order_detail.total_price = order_detail.price_at_sale * order_detail.quantity
    order_detail.total_after_discount = order_detail.total_price * (1 - Decimal(row['Discount']))
    order_detail.save()
    return order_detail


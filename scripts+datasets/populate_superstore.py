import os
import sys
import django
import csv
from decimal import Decimal

sys.path.append('../../cm3035midterm')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cm3035midterm.settings')
django.setup()

#Importing the models from superstore/models.py
from superstore.models import *
#iomporting the functions from populate_functions.py
from populate_functions import *

data_file = 'post-script-superstore.csv'

with open(data_file, mode='r', newline='', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file, delimiter=',')
    row_counter = 0

    #Deleting all data (starting from referencing to referenced) currently in the database before populating
    OrderDetails.objects.all().delete()
    Orders.objects.all().delete()
    Customers.objects.all().delete()
    Products.objects.all().delete()
    Addresses.objects.all().delete()

    for row in csv_reader:
        row_counter += 1
        try:
            try:
                postal_code = row['Postal Code']
                if not Addresses.objects.filter(postal_code=postal_code).exists():
                    create_address(row)
                else:
                    print(f"Address already exists at row {row_counter}")
            except Exception as e:
                print(f"Error in Address at row {row_counter}: {e}")

            try:
                product = row['Product ID']
                if not Products.objects.filter(product_id=product).exists():
                    create_product(row)
                else:
                    print(f"Product already exists at row {row_counter}")
            except Exception as e: 
                print(f"Error in Customer at row {row_counter}: {e}")

            try:
                customer = row['Customer ID']
                if not Customers.objects.filter(customer_id=customer).exists():
                    create_customer(row)
                else:
                    print(f"Customer already exists at row {row_counter}")
            except Exception as e:  
                print(f"Error in Product at row {row_counter}: {e}")
            
            try: 
                order = row['Order ID']
                if not Orders.objects.filter(order_id=order).exists():
                    create_order(row)
                else:
                    print(f"Order already exists at row {row_counter}")
            except Exception as e: 
                print(f"Error in Order at row {row_counter}: {e}")

            try:
                create_order_detail(row)
            except Exception as e:  
                print(f"Error in OrderDetail at row {row_counter}: {e}")
            
            print(f'Successfully processed row {row_counter}')

        except Exception as e:
            print(f"An error occurred at row {row_counter}: {e}")

print('Script completed')

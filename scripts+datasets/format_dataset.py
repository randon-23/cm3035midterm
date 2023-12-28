import csv;
from collections import defaultdict;

fieldnames = [
    'Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 'Customer ID',
    'Customer First Name', 'Customer Last Name', 'Segment', 'Country', 'City', 'State', 'Postal Code',
    'Region', 'Product ID', 'Category', 'Sub-Category', 'Product Name',
    'Product Info', 'Unit Price', 'Total Price', 'Quantity', 'Discount', 'Total After Discount'
]

def load_csv(filename):
    with open(filename, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def save_csv(filename, data, fieldnames):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def format_data(data):
    customer_locations = defaultdict(dict)

    for row in data:
        if ',' in row['Product Name']:
            product_name, product_info = row['Product Name'].split(',', 1)
            row['Product Name'] = product_name.strip()
            row['Product Info'] = product_info.strip()

        customer_first_name, customer_last_name = row['Customer Name'].split(' ', 1)
        row['Customer First Name'] = customer_first_name.strip()
        row['Customer Last Name'] = customer_last_name.strip()

        customer_id=row['Customer ID']
        if customer_id not in customer_locations:
            customer_locations[customer_id] = {
                'City': row['City'],
                'State': row['State'],
                'Postal Code': row['Postal Code']
            }
        else:
            row['City'] = customer_locations[customer_id]['City']
            row['State'] = customer_locations[customer_id]['State']
            row['Postal Code'] = customer_locations[customer_id]['Postal Code']

        if row['Discount'] != '0':
            row['Total Price'] = float(row['Unit Price'])*int(row['Quantity'])
            row['Total After Discount'] = float(row['Total Price'])*(1-float(row['Discount']))
        else:
            row['Total Price'] = float(row['Unit Price'])*int(row['Quantity'])
            row['Total After Discount'] = row['Total Price']
        row.pop('Customer Name', None)

    return data

inputfile = 'pre-script-superstore.csv'
outputfile = 'post-script-superstore.csv'

dataset = load_csv(inputfile)

formatted_data = format_data(dataset)

save_csv(outputfile, formatted_data, fieldnames)
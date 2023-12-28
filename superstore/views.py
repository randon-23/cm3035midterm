from django.shortcuts import render
from django.views.generic import *
import json
from .models import *
from .forms import *
from .api import *

def index(request):
    products = Products.objects.all()
    return render(request, 'index.html', {'products': products})

# This file contains the views for the application. It is this way because I have elected to seperate logically the APIs (api.py) and the views.
# Each view function is responsible for handling user requests and rendering the appropriate response. However, the actual data processing and business logic is handled separately by the API views in api.py.
# When a view function needs to perform an operation such as creating an order, rendering a form, or fetching data, it makes a call to the corresponding API endpoint. The API then processes the request and returns the result back to the view function.

#Endpoint 1 - POST ORDER
def create_order_view(request):
    #We are rendering the form here, the template is responsible for making the API call and handling its response (i.e. resetting the form to its initial state)
    order_form = OrderForm()
    order_details_form = OrderDetailsForm()
    return render(request, 'create_order.html', {'order_form': order_form, 'order_details_form': order_details_form})

#Endpoint 2 - GET ORDER
def get_order_view(request, order_id):
    response = get_order_details_api(request, order_id)
    if response.status_code == 200:
        order = json.loads(response.content)
        return render(request, 'order.html', {'order': order})
    else:
        return JsonResponse({"error": "Order not found"}, status=404)

#Endpoint 3 - GET FILTER PRODUCTS FORM & GET FILTERED PRODUCTS API CALL
def get_filter_products_form_view(request):
    #In this type of endpoint we are solely rendering the form, the follwowing view function is responsible for making the API call and handling its response
    filter_products_form = ProductsForm()
    return render(request, 'get_filter_products_form.html', {'filter_products_form': filter_products_form})

def get_filtered_products_view(request):
    response = get_filter_products_api(request)
    if response.status_code == 200:
        products = json.loads(response.content)
        return render(request, 'filtered_products.html', {'products': products})
    else:
        return JsonResponse({"error": "Order not found"}, status=404)

#Endpoint 4 - GET REVENUE LOCATION FORM & GET REVENUE FROM A GIVEN LOCATION API CALL
def get_revenue_location_form_view(request):
    #In this type of endpoint we are solely rendering the form, the follwowing view function is responsible for making the API call and handling its response
    locations_form = LocationsForm()
    return render(request, 'get_revenue_location_form.html', {'locations_form': locations_form})

def get_revenue_location_view(request):
    response = get_revenue_location_api(request)
    if response.status_code == 200:
        results = json.loads(response.content)
        return render(request, 'revenue_location.html', {'results': results})
    else:
        results = json.loads(response.content)
        return render(request, 'revenue_location.html', {'results': results})
    
#Endpoint 5 - GET CUSTOMERS PURCHASE HISTORY
def get_customer_orders_view(request, customer_id):
    response = get_customer_orders_api(request, customer_id)
    if response.status_code == 200:
        orders = json.loads(response.content)
        return render(request, 'customer_orders.html', {'orders': orders})
    else:
        return JsonResponse({"error": "Customer not found"}, status=404)
    
#Endpoint 6 - UPDATE SHIP DATE FOR AN ORDER
def update_ship_date_form_view(request, order_id):
    ship_date_form = ShipDateForm()
    return render(request, 'update_ship_date_form.html', {'ship_date_form': ship_date_form, 'order_id': order_id})
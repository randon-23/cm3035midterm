from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
import random
import datetime

#Here I am showing taht I can use the Django ORM to query the database and return the results in JSON format and on the DRF web browsable API
# @api_view(['GET'])
# def get_order_details_api(request, order_id):
#     try:
#         order = Orders.objects.get(order_id=order_id)
#     except Orders.DoesNotExist:
#         HttpResponse(status=404)
#     if request.method == 'GET':
#         order_serializer = OrdersSerializer(order)
#         order_details_dict = dict(order_serializer.data)

#         grand_total = sum(int(detail['total_after_discount']) for detail in order_details_dict['order_details'])
#         order_details_dict['grand_total'] = grand_total

#         return render(request, 'order.html', {'order': order_details_dict})

#This is the API endpoint for getting the details of a specific order and rendering the response
#in the DRF web browsable API
# @api_view(['GET'])
# def get_order_details_api(request, order_id):
#     try:
#         orders = Orders.objects.get(order_id=order_id)
#     except Orders.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         order_serializer = OrdersSerializer(orders)
#         return Response(order_serializer.data, status=status.HTTP_200_OK)
    
# This is the API endpoint for getting the details of a specific order and returning the response
# in JSON format
@api_view(['GET'])
def get_order_details_api(request, order_id):
    try:
        order = Orders.objects.get(order_id=order_id)
    except Orders.DoesNotExist:
        Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        order_serializer = OrdersSerializer(order)
        order_details_dict = dict(order_serializer.data)

        grand_total = sum(float(detail['total_after_discount']) for detail in order_details_dict['order_details'])
        order_details_dict['grand_total'] = grand_total

        return JsonResponse(order_details_dict, status=status.HTTP_200_OK)

# This function defines an API endpoint for creating a new order.
@api_view(['GET', 'POST'])
def create_order_api(request=None):
    if request.method == 'POST':
        # Making a mutable copy of the data, used to create the new order
        data = request.data.copy() 
        
        # Setting order_id and order_date prior to serializer validation
        order_id = "UOL-"+str(datetime.date.today().year)+"-"+str(random.randint(100000, 999999))
        while Orders.objects.filter(order_id=order_id).exists():
            order_id = "UOL-"+str(datetime.date.today().year)+"-"+str(random.randint(100000, 999999))
        data['order_id'] = order_id

        data['order_date'] = datetime.date.today()
        # For each order detail(item) in the order, it retrieves the corresponding product from the Products model. 
        # It then sets the product_name and price_at_sale in the order detail to the product's name and unit price, respectively. 
        # It also calculates the total price for the order detail by multiplying the product's unit price by the quantity.
        for detail in data['order_details']:
            product = Products.objects.get(product_id=detail['product'])
            detail['product_name'] = product.product_name
            detail['price_at_sale'] = product.product_unit_price
            detail['total_price'] = product.product_unit_price * int(detail['quantity'])

        # New serializer created with the modified data
        # If valid, the new order is saved to the database and the response is returned
        order_serializer = OrdersSerializer(data=data)

        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response(status=status.HTTP_200_OK)

# This is a Django ListView for getting the list of all orders
class GetOrdersList(ListView):
    model = Orders
    template_name = 'get_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    #Return orders most recent first
    def get_queryset(self):
        return Orders.objects.all().order_by('-order_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = self.request.GET.get('update', 'false').lower() == 'true'
        return context

#This is a Django ListView for getting a list of all cutomers
class GetCustomersList(ListView):
    model = Customers
    template_name = 'get_customers.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        return Customers.objects.all().order_by('customer_last_name')

#This function defines an API endpoint that allows clients to filter products based on certain criteria.
# It uses Django Q objects to build a dynamic query for the filter.
@api_view(['GET'])
def get_filter_products_api(request):
    product_category = request.GET.get('product_category', '')
    product_sub_category = request.GET.get('product_sub_category', '')
    product_unit_price = request.GET.get('product_unit_price', '')
    comparison = request.GET.get('comparison', '')

    filters = Q()
    if product_category != '':
        filters &= Q(product_category=product_category)
    if product_sub_category != '':
        filters &= Q(product_sub_category=product_sub_category)
    if product_unit_price != '' and comparison != '':
        product_unit_price = float(product_unit_price)
        if comparison == '>':
            filters &= Q(product_unit_price__gt=product_unit_price)
        elif comparison == '<':
            filters &= Q(product_unit_price__lt=product_unit_price)
        elif comparison == '=':
            filters &= Q(product_unit_price=product_unit_price)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    if (product_unit_price != '' and comparison == '') or (product_unit_price == '' and comparison != ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    products = Products.objects.filter(filters)
    products_serializer = ProductsSerializer(products, many=True)
    return JsonResponse(products_serializer.data, safe=False, status=status.HTTP_200_OK)

#This function defines an API endpoint that allows users to get the total revenue for a specific location
#It uses Django Q objects to build a dynamic query for the filter.
#The location can be specified using any of the following parameters: region, city, state or postal_code (seperately)
@api_view(['GET'])
def get_revenue_location_api(request):
    region = request.GET.get('region','')
    city = request.GET.get('city', '')
    state = request.GET.get('state', '')
    postal_code = request.GET.get('postal_code', '')

    if len([param for param in [region, city, state, postal_code] if param != '']) != 1:
        return JsonResponse({"error": "Strictly provide one input parameter from region, city, state or postal_code"},status=status.HTTP_400_BAD_REQUEST)

    filters = Q()
    if region != '':
        filters &= Q(customer__address__region=region)
    elif city != '':
        filters &= Q(customer__address__city=city)
    elif state != '':
        filters &= Q(customer__address__state=state)
    elif postal_code != '':
        filters &= Q(customer__address__postal_code=postal_code)
    
    orders = Orders.objects.filter(filters)
    orders_serializer = OrdersSerializer(orders, many=True)
    
    #Calculating the total revenue for the location after the orders have been filtered and serialized, as the total revenue is not stored in the database
    total_revenue = sum(round(detail['total_after_discount'], 2) for order in orders_serializer.data for detail in order['order_details'])
    return JsonResponse({"orders": orders_serializer.data, "total_revenue": total_revenue}, status=status.HTTP_200_OK)

#This function defines an API endpoint that allows users to get the purchase history of a given customer
@api_view(['GET'])
def get_customer_orders_api(request, customer_id):
    try:
        customer = Customers.objects.get(customer_id=customer_id)
    except Customers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        orders = Orders.objects.filter(customer=customer)
        orders_serializer = OrdersSerializer(orders, many=True)
        return JsonResponse(orders_serializer.data, safe=False, status=status.HTTP_200_OK)

# This function defines an API endpoint that allows clients to update the ship date of an existing order.
# Not all clients support PATCH requests, so I have also allowed POST requests for this endpoint.
@api_view(['GET', 'POST', 'PATCH'])
def update_ship_date_api(request, order_id):
    if request.method == 'POST' or request.method == 'PATCH':
        #It creates a new UpdateOrderSerializer with the request data. This partial serializer is used to validate the new ship date.
        update_serializer = UpdateOrderSerializer(data=request.data)
        if update_serializer.is_valid():
            try:
                order = Orders.objects.get(order_id=order_id)
            except Orders.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            order.ship_date = update_serializer.validated_data['ship_date']
            order.save()
            return Response(update_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(update_serializer.data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
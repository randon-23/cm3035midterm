from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    #Rendering Views

    path('', views.index, name='index'),
    path('create_order/', views.create_order_view, name='create_order_view'),
    path('get_orders/<str:order_id>', views.get_order_view, name='get_order_view'),
    path('get_filter_products_form/', views.get_filter_products_form_view, name='get_filter_products_form_view'),
    path('get_filtered_products/', views.get_filtered_products_view, name='get_filtered_products_view'),
    path('get_revenue_location_form/', views.get_revenue_location_form_view, name='get_revenue_location_form_view'),
    path('get_revenue_location/', views.get_revenue_location_view, name='get_revenue_location_view'),
    path('get_customer_orders/<str:customer_id>', views.get_customer_orders_view, name='get_customer_orders_view'),
    path('update_ship_date_form_view/<str:order_id>', views.update_ship_date_form_view, name='update_ship_date_form_view'),


    #API endpoint views - These views directly call the API endpoints. In the application these are called via views.py functions or by the fetch API in the templates in case of POST requests

    #POST - Endpoint 1 - This endpoint is fetched via fetch API in the template 'create_order.html
    # This is due to the architecture of my dataset which had multiple orderDetails (order items) per order
    # Therefore listeners were added to both forms to prevent their default behaviour, instead save the orderDetails in the session
    # And then once the order form is submitted, we can submit all orderDetails in the session to the API, under the umbrella of the order

    path('api/create_order/', api.create_order_api, name='create_order_api'),
    #GET - Endpoint 2
    path('api/get_orders/', api.GetOrdersList.as_view(), name='get_orders_api'),
    #GET - Endpoint 2
    path('api/get_orders/<str:order_id>', api.get_order_details_api, name='get_order_details_api'),
    #GET - Endpoint 3
    path('api/get_filter_products/', api.get_filter_products_api, name='get_filter_products_api'),
    #GET - Endpoint 4
    path('api/get_revenue_location/', api.get_revenue_location_api, name='get_revenue_location_api'),
    #GET - Endpoint 5
    path('api/get_customers/', api.GetCustomersList.as_view(), name='get_customers_api'),
    #GET - Endpoint 5
    path('api/get_customer_orders/<str:customer_id>', api.get_customer_orders_api, name='get_customer_orders_api'),
    #POST/PATCH - Endpoint 6
    path('api/update_ship_date_api/<str:order_id>', api.update_ship_date_api, name='update_ship_date_api'),
]
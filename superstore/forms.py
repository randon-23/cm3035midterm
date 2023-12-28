from django import forms
from .models import *
from datetime import datetime

class OrderForm(forms.ModelForm):
    #Here we are using an alternative form of validation for ship_mode and customer
    #by overriding the __init__ method and pre-populating the fields with the choices
    #and queryset respectively
    SHIP_MODE_CHOICES = [
        ('Standard Class', 'Standard Class'),
        ('Second Class', 'Second Class'),
        ('First Class', 'First Class'),
        ('Same Day', 'Same Day'),
    ]

    class Meta:
        model = Orders
        fields = ['ship_mode', 'customer']
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['ship_mode'] = forms.ChoiceField(choices=self.SHIP_MODE_CHOICES)
        self.fields['customer'] = forms.ModelChoiceField(queryset=Customers.objects.all())

#This form is used to select the orderDetails (order items) and quantity for the order which is being created
class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super(OrderDetailsForm, self).__init__(*args, **kwargs)
        #Dropdown list of all products in database
        self.fields['product'] = forms.ModelChoiceField(queryset=Products.objects.all())

#This form is used to filter products based on their category, sub-category, and unit price.
#The category and sub-category fields are ChoiceFields, which means they will generate dropdown menus with all the distinct categories and sub-categories in the database.
class ProductsForm(forms.ModelForm):
    OPERATOR_CHOICES = [
        ('', '---------'),
        ('=', 'equals'),
        ('<', 'smaller than'),
        ('>', 'greater than'),
    ]
    comparison = forms.ChoiceField(choices=OPERATOR_CHOICES)

    class Meta:
        model = Products
        fields = ['product_category', 'product_sub_category', 'product_unit_price']
    
    def __init__(self, *args, **kwargs):
        super(ProductsForm, self).__init__(*args, **kwargs)
        #The category and sub-category fields are ChoiceFields, which means they will generate dropdown menus with all the distinct categories and sub-categories in the database + a default empty option
        self.fields['product_category'] = forms.ChoiceField(
            choices=[('', '-----------')] +list(Products.objects.values_list('product_category', 'product_category').distinct())
        )
        self.fields['product_sub_category'] = forms.ChoiceField(
            choices=[('', '-----------')]+list(Products.objects.values_list('product_sub_category', 'product_sub_category').distinct())
        )
        #DecimalField for unit price
        self.fields['product_unit_price'] = forms.DecimalField(max_digits=10, decimal_places=2)

#Form which is used to filter orders and resulting total revenue by location(region, state, city, zip_code)
#Error handling in the API view which listens for calls from this form returns an error message if the user selects more than 1 field to filter by
class LocationsForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = ['city', 'state', 'region', 'postal_code']

    def __init__(self, *args, **kwargs):
        super(LocationsForm, self).__init__(*args, **kwargs)
        self.fields['city'] = forms.ChoiceField(
            choices=[('', '-----------')] +list(Addresses.objects.values_list('city', 'city').distinct())
        )
        self.fields['state'] = forms.ChoiceField(
            choices=[('', '-----------')] +list(Addresses.objects.values_list('state', 'state').distinct())
        )
        self.fields['region'] = forms.ChoiceField(
            choices=[('', '-----------')] +list(Addresses.objects.values_list('region', 'region').distinct())
        )
        self.fields['postal_code'] = forms.ChoiceField(
            choices=[('', '-----------')] +list(Addresses.objects.values_list('postal_code', 'postal_code').distinct())
        )

#Form which is used to update the ship date of an order
#DateField with a DateInput widget which allows the user to select a date from a calendar in the format which is understood by the underlying database
class ShipDateForm(forms.ModelForm):
    ship_date = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}),
                                help_text="Updates will be submitted in the following format: <em>YYYY-MM-DD</em>.")

    class Meta:
        model = Orders
        fields = ['ship_date']
    
    def clean_ship_date(self):
        ship_date = self.cleaned_data['ship_date']
        if ship_date < datetime.today().date():
            raise forms.ValidationError("Ship date cannot be before order date")
        return ship_date
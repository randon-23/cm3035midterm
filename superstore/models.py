from django.db import models

class Addresses(models.Model):
    address_id = models.AutoField(null=False, blank=False, primary_key=True)
    region = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(max_length=255, null=False, blank=False)
    country = models.CharField(max_length=255, null=False, blank=False)
    postal_code = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return f"{self.postal_code}"

class Products(models.Model):
    product_id = models.CharField(max_length=255, null=False, blank=False, primary_key=True)
    product_name = models.CharField(max_length=255, null=False, blank=False)
    product_info = models.CharField(max_length=255, null=False, blank=False)
    product_category = models.CharField(max_length=255, null=False, blank=False)
    product_sub_category = models.CharField(max_length=255, null=False, blank=False)
    product_unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    #Upon delete, we update the product_name in OrderDetails to include (Deleted) such that future references will give user valid context
    def delete(self, *args, **kwargs):
        OrderDetails.objects.filter(product_id=self.product_id).update(product_name=self.product_name + ' (Deleted)')
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.product_id} - {self.product_name}"

class Customers(models.Model):
    customer_id = models.CharField(max_length=255, null=False, blank=False, primary_key=True)
    customer_first_name = models.CharField(max_length=255, null=False, blank=False)
    customer_last_name = models.CharField(max_length=255, null=False, blank=False)
    customer_segment = models.CharField(max_length=255, null=False, blank=False)
    address = models.ForeignKey(Addresses, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.customer_id} - {self.customer_first_name} {self.customer_last_name}"

class Orders(models.Model):
    order_id = models.CharField(max_length=255, null=False, blank=False, primary_key=True)
    order_date = models.DateField(null=False, blank=False)
    #ship_date can be null because it is possible that the order has not been shipped yet
    #However, it cannot be blank because we need to know when the order was shipped
    #Additionally, ship_mode cannot be null nor blank because we need to know what shipping mode the customer chose
    ship_date = models.DateField(null=True, blank=False)
    ship_mode = models.CharField(max_length=255, null=False, blank=False)
    customer = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.order_id}"


#product_name is used to store the product name in case the product is deleted from the database. Therefore, for integrity purposes, it is not a foreign key
#Therefore, we need to override the save method to ensure that product_name is always set to the product_name of the product
#Additionally, this class variable is what we will always use, deleted or not, to display the product name
class OrderDetails(models.Model):
    order_detail_id = models.AutoField(null=False, blank=False, primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00)
    total_after_discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def save(self, *args, **kwargs):
        if not self.product_name:
            self.product_name = self.product.product_name
        if not self.price_at_sale:
            self.price_at_sale = self.product.product_unit_price
        if self.discount != 0.00:
            self.total_after_discount = self.total_price * (1 - self.discount)
        else:
            self.total_after_discount = self.total_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order.order_id} - {self.product_name}"


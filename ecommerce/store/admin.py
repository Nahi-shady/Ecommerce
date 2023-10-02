from django.contrib import admin
from .models import *

# Register your models here.

admin.register(Customer)
admin.register(Product)
admin.register(Order)
admin.register(OrderItem)
admin.register(ShippingAddress)
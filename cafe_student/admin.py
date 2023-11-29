from django.contrib import admin
from .models import Type_Product, Product, Order
# Register your models here.


admin.site.register(Type_Product)
admin.site.register(Product)
admin.site.register(Order)
from django.contrib import admin
from .models import Product
# Register your models here.

#njoubuha mel models li hya class naamlouha création fel model
admin.site.register(Product) # table creation in the database witch i can create the CRUD operation.

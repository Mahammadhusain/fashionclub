from django.contrib import admin
from .models import CategoryModel,ProductModel,CustomerModel,Cart,Order
# Register your models here.


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id","name"]

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["description", "price", "name", "image", "category","id"]
    list_display.reverse()



@admin.register(CustomerModel)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ["id","state", "zipcode", "city", "locality", "name", "user"]
    list_display.reverse()
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["quantity", "product", "user"]
    list_display.reverse()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["status", "order_date", "quantity", "product", "customer", "user"]
    list_display.reverse()



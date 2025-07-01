from django.contrib import admin
from .models import Product, Order, Cart, CartItem, TableBooking

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    list_filter = ('name',)

    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product', 'quantity', 'total_price', 'created_at')
    list_filter = ('created_at',)

    def customer_name(self, obj):
        return obj.customer.name


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(TableBooking)
# admin.site.register(Customer)

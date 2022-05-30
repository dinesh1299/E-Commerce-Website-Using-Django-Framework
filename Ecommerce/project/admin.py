from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(CancelOrder)

#admin.site.register(ShippingAddress)

class CustomerInline(admin.StackedInline):
    model=Customer
    can_delete=False

class CustomisedUserAdmin(UserAdmin):
    inlines=(CustomerInline,)
admin.site.unregister(User)
admin.site.register(User,CustomisedUserAdmin)    

class OrderInline(admin.TabularInline):
    model=OrderItem
    can_delete=False

class CustomizedOrder(admin.ModelAdmin):
    model=Order
    inlines=(OrderInline,)

admin.site.register(Order,CustomizedOrder)
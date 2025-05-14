from django.contrib import admin
from shop.models import Product,Cart, CartItem, Order, OrderItem

# Register your models here.
admin.site.register(Product)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'price', 'quantity', 'total_price']
    readonly_fields = ['price', 'total_price']

    def price(self, obj):
        return obj.product.price
    price.short_description = 'Price'

    def total_price(self, obj):
        return obj.get_total_price()
    total_price.short_description = 'Total Price'

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('formatted_user', 'created_at', 'status')  # Add status to the list display
    # actions = ['mark_as_complete']

    def formatted_user(self, obj):
        return f"Cart of {obj.user.username}"
    formatted_user.short_description = 'User'

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price', 'total_price')
    readonly_fields = ['price', 'total_price']

    def price(self, obj):
        return obj.product.price
    price.short_description = 'Price'

    def total_price(self, obj):
        return obj.get_total_price()
    total_price.short_description = 'Total Price'

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price', 'total_price')
    readonly_fields = ['price', 'total_price']

    def price(self, obj):
        return obj.product.price
    price.short_description = 'Price'

    def total_price(self, obj):
        return obj.get_total_price()
    total_price.short_description = 'Total Price'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing item
            return ['cart', 'price', 'total_price']  # Read-only fields
        else:
            return self.readonly_fields

admin.site.register(Cart, CartAdmin)



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'price', 'quantity', 'total_price']
    readonly_fields = ['price', 'total_price']

    def price(self, obj):
        return obj.product.price
    price.short_description = 'Price'

    def total_price(self, obj):
        return obj.get_total_price()
    total_price.short_description = 'Total Price'

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('formatted_user', 'created_at', 'status')  # Add status to the list display
    # actions = ['mark_as_complete']

    def formatted_user(self, obj):
        return f"Order of {obj.user.username}"
    formatted_user.short_description = 'User'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('Order', 'product', 'quantity', 'price', 'total_price')
    readonly_fields = ['price', 'total_price']

    def price(self, obj):
        return obj.product.price
    price.short_description = 'Price'

    def total_price(self, obj):
        return obj.get_total_price()
    total_price.short_description = 'Total Price'

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('Order', 'product', 'quantity', 'price', 'total_price')
    readonly_fields = ['price', 'total_price']

    def price(self, obj):
        return obj.product.price
    price.short_description = 'Price'

    def total_price(self, obj):
        return obj.get_total_price()
    total_price.short_description = 'Total Price'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing item
            return ['Order', 'price', 'total_price']  # Read-only fields
        else:
            return self.readonly_fields

admin.site.register(Order, OrderAdmin)
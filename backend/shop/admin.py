from django.contrib import admin
from .models import (
    Category, Tag, Product, ProductImage, Review,
    Cart, CartItem, Wishlist, Address, Order, OrderItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'sku', 'description']
    list_editable = ['price', 'stock', 'is_featured', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['tags']
    inlines = [ProductImageInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_verified_purchase']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'quantity', 'unit_price', 'line_total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['order_number', 'user__email', 'shipping_name']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'user', 'status', 'notes')}),
        ('Shipping', {'fields': (
            'shipping_method', 'shipping_name', 'shipping_phone',
            'shipping_street', 'shipping_city', 'shipping_state',
            'shipping_postal_code', 'shipping_country', 'tracking_number',
        )}),
        ('Payment', {'fields': ('subtotal', 'shipping_cost', 'tax', 'total', 'is_paid', 'paid_at', 'stripe_payment_intent')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

from rest_framework import serializers
from .models import (
    Category, Tag, Product, ProductImage, Review,
    Cart, CartItem, Wishlist, Address, Order, OrderItem
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'product_count']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'rating', 'title', 'body',
                  'is_verified_purchase', 'created_at']
        read_only_fields = ['is_verified_purchase', 'created_at']

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.email.split('@')[0]


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    discount_percent = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price',
            'compare_price', 'discount_percent', 'image', 'category_name',
            'average_rating', 'review_count', 'is_in_stock', 'is_featured',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    discount_percent = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'compare_price', 'discount_percent', 'stock',
            'sku', 'image', 'images', 'category', 'tags', 'weight',
            'is_in_stock', 'is_featured', 'average_rating', 'review_count',
            'reviews', 'created_at',
        ]


# ─── Cart ─────────────────────────────────────────────────────────────────────

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        source='product',
        write_only=True
    )
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'line_total']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'subtotal']


# ─── Address ──────────────────────────────────────────────────────────────────

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user']


# ─── Order ────────────────────────────────────────────────────────────────────

class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_sku',
                  'quantity', 'unit_price', 'line_total']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'shipping_method',
            'shipping_name', 'shipping_phone', 'shipping_street',
            'shipping_city', 'shipping_state', 'shipping_postal_code',
            'shipping_country', 'subtotal', 'shipping_cost', 'tax',
            'total', 'is_paid', 'paid_at', 'tracking_number',
            'notes', 'items', 'created_at',
        ]
        read_only_fields = ['order_number', 'status', 'is_paid', 'paid_at', 'tracking_number']


class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField(required=False)
    shipping_name = serializers.CharField(max_length=200, required=False)
    shipping_phone = serializers.CharField(max_length=20, required=False)
    shipping_street = serializers.CharField(max_length=300)
    shipping_city = serializers.CharField(max_length=100)
    shipping_state = serializers.CharField(max_length=100)
    shipping_postal_code = serializers.CharField(max_length=20)
    shipping_country = serializers.CharField(max_length=100, default='US')
    shipping_method = serializers.ChoiceField(choices=['standard', 'express', 'overnight'], default='standard')
    notes = serializers.CharField(required=False, allow_blank=True)

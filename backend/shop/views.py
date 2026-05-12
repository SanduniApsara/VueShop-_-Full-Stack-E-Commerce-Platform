from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from decimal import Decimal
import stripe
from django.conf import settings

from .models import (
    Category, Product, Review, Cart, CartItem,
    Wishlist, Address, Order, OrderItem
)
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ReviewSerializer, CartSerializer, CartItemSerializer,
    AddressSerializer, OrderSerializer, CreateOrderSerializer
)
from .filters import ProductFilter

stripe.api_key = settings.STRIPE_SECRET_KEY

SHIPPING_COSTS = {
    'standard': Decimal('5.99'),
    'express': Decimal('12.99'),
    'overnight': Decimal('24.99'),
}
TAX_RATE = Decimal('0.08')  # 8%


# ─── Category ─────────────────────────────────────────────────────────────────

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


# ─── Product ──────────────────────────────────────────────────────────────────

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('tags', 'images', 'reviews')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name', 'tags__name']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        qs = self.get_queryset().filter(is_featured=True)[:8]
        serializer = ProductListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def reviews(self, request, slug=None):
        product = self.get_object()
        if request.method == 'POST':
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


# ─── Cart ─────────────────────────────────────────────────────────────────────

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartItemView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id, is_active=True)

        if product.stock < quantity:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemUpdateView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(CartItem, id=self.kwargs['pk'], cart__user=self.request.user)

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        if quantity <= 0:
            item.delete()
        else:
            if item.product.stock < quantity:
                return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
            item.quantity = quantity
            item.save()
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart, context={'request': request}).data)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart, context={'request': request}).data)


# ─── Wishlist ─────────────────────────────────────────────────────────────────

class WishlistView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        products = ProductListSerializer(wishlist.products.all(), many=True, context={'request': request})
        return Response({'products': products.data})

    def post(self, request):
        product = get_object_or_404(Product, id=request.data.get('product_id'))
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            return Response({'status': 'removed'})
        else:
            wishlist.products.add(product)
            return Response({'status': 'added'})


# ─── Address ──────────────────────────────────────────────────────────────────

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─── Order ────────────────────────────────────────────────────────────────────

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        shipping_method = data.get('shipping_method', 'standard')
        subtotal = cart.subtotal
        shipping_cost = SHIPPING_COSTS[shipping_method]
        tax = subtotal * TAX_RATE
        total = subtotal + shipping_cost + tax

        order = Order.objects.create(
            user=request.user,
            shipping_method=shipping_method,
            shipping_name=data.get('shipping_name', request.user.get_full_name()),
            shipping_phone=data.get('shipping_phone', ''),
            shipping_street=data['shipping_street'],
            shipping_city=data['shipping_city'],
            shipping_state=data['shipping_state'],
            shipping_postal_code=data['shipping_postal_code'],
            shipping_country=data.get('shipping_country', 'US'),
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            total=total,
            notes=data.get('notes', ''),
        )

        for item in cart.items.select_related('product').all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_sku=item.product.sku,
                quantity=item.quantity,
                unit_price=item.product.price,
            )
            item.product.stock -= item.quantity
            item.product.save()

        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class CreatePaymentIntentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user, is_paid=False)
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),
                currency='usd',
                metadata={'order_id': order.id, 'user_id': request.user.id},
            )
            order.stripe_payment_intent = intent['id']
            order.save()
            return Response({'client_secret': intent['client_secret']})
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

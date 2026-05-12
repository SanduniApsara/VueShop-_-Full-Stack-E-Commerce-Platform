from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('products', views.ProductViewSet, basename='product')
router.register('addresses', views.AddressViewSet, basename='address')
router.register('orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    # Cart
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.CartItemView.as_view(), name='cart-add'),
    path('cart/update/<int:pk>/', views.CartItemUpdateView.as_view(), name='cart-update'),
    # Wishlist
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    # Orders
    path('orders/create/', views.CreateOrderView.as_view(), name='order-create'),
    path('orders/<int:order_id>/payment-intent/', views.CreatePaymentIntentView.as_view(), name='payment-intent'),
]

from django.urls import path 
from . import views



urlpatterns = [

    path ('users/profile', views.getUserProfile, name='user-profile'),
    path ('users/profile/update', views.updateUserProfile, name='user-profile-update'),
    
    # Товары
    path ('products', views.getProducts, name='products'),
    path ('products/<str:pk>', views.getProduct, name='product'),
    
    # Заказы
    path ('orders/add', views.addOrderItems, name='order-add'),
    path('my_orders', views.getMyOrders, name='my-orders'),
    path('order/<str:pk>', views.getOrderById, name='get-order-by-id'),

     
]

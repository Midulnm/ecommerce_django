from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_history, name='order_history'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]

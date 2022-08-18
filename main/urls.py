from django.urls import path
from . import views

urlpatterns = [
	path('', views.indexHandler, name='index'),
	path('cart', views.cartHandler, name='cart'),
	path('products/', views.productsHandler, name='store'),
	path('products/<int:product_id>', views.productHandler),
	path('orders/', views.orderHandler, name='orders'),
	path('orders/<int:order_id>', views.orderItemHandler),
]

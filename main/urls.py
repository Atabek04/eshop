from django.urls import path
from . import views

urlpatterns = [
	path('', views.indexHandler, name='index'),
	path('products/', views.productsHandler, name='store'),
	path('products/<int:product_id>', views.productHandler)
]
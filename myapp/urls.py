from django.urls import path
from . import views # импорт представлений из текущего пакета
from .views import index, about, error_404, client_orders_post

# настройка маршрутов

urlpatterns = [
    path('', views.index, name='index'), # путь к представлению index
    path('about/', views.about, name='about'), # путь к представлению about
    path('error_404/', views.error_404, name='error_404'), # путь к представлению error_404
    path('clients/<int:client_id>/', views.client_orders_post, name='client_orders'), # путь к представлению client_orders
    path('clients/all/', views.clients_all, name='clients_all'), # путь к представлению clients_all
    path('client_about/<int:client_id>/', views.client_about, name='client_about'), # путь к представлению client_about
    path('products/<int:product_id>/', views.product_full, name='product_full'),
    path('clients/add/', views.add_user, name='add_user'), # Добавление клиента HW-4 25.04.24
    path('products/add/', views.add_product, name='add_product'), # Добавление товара HW-4 25.04.24
    path('products/info/<int:product_id>/', views.product_info, name='product_info'), # Отображение информации о товаре HW-4 25.04.24
    path('category/', views.category_all, name='category_all'), # Отображение всех категорий HW-4 25.04.24
    path('products/category/<str:category>/', views.product_category, name='product_category'), # Отображение товаров по категориям HW-4 25.04.24
]
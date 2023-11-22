from django.urls import path, include
from my_app import views


app_name = 'my_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('user_login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('regular_customer/', views.regular_customer, name='regular_customer'),
    path('site_admin/', views.site_admin, name='site_admin'),
    path('supplier/', views.supplier, name='supplier'),
    path('drugstore/', views.drugstore, name='drugstore'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_user_product_admin/', views.add_user_product_admin, name='add_user_product_admin'),
    path('add_user_product_supplier/', views.add_user_product_supplier, name='add_user_product_supplier'),
    path('add_order_regualr_customer/', views.add_order_regular_customer, name='add_order_regular_customer'),
    path('search_order_view/', views.search_order_view, name='search_order_view'),
    path('search_order/', views.search_order, name='search_order'),
    path('search_movement_view/', views.search_movement_view, name='search_movement_view'),
    path('search_movement/', views.search_movement, name='search_movement'),
    path('get_form_info/', views.get_form_info, name='get_form_info'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('index_login/', views.index_login, name='index_login'),


]
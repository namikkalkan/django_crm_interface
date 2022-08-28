from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('user/', views.userPage, name='user_page'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('update_customer/<str:pk>/', views.updateCustomer, name='update_customer'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:ppk>/', views.deleteOrder, name="delete_order"),
    path('create_customer/', views.createCustomer, name="create_customer"),
    path('delete_customer/<str:ppk>/', views.deleteCustomer, name="delete_customer"),
                ]
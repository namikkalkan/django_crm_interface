from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('account/', views.accountSettings, name="account_settings"),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>//', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('reset_password_completed/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

                ]
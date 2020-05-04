from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),

    path('customer/<str:pk>/', views.customer, name='customer'),
    path('create_customer/', views.createCustomer, name='create_customer'),
    path('update_customer/<str:pk>/', views.updateCustomer, name='update_customer'),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name='delete_customer'),

    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

    path('signup/', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('signout/', views.signOut, name='signout'),

    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account'),



    path('purchase/<str:pk>/', views.newOrderCustomer, name='purchase'),
    path('payment/<str:pk>/', views.payment, name='payment'),


    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'),
        name='reset_password'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/reset_password_form.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_done.html'),
         name='password_reset_complete')

]

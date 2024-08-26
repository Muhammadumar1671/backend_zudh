from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment/success?success=true', views.payment_success, name='payment_success'),
    path('unsuccessful?canceled=true' , views.payment_cancel, name='payment_cancel'),
    path('stripe_checkout_page/', views.stripe_checkout_page, name='stripe_checkout_page'),
]


from django.urls import path
from . import views

app_name = 'suit'

urlpatterns = [
    path('create_suit/', views.create_suit, name='create_suit'),
]
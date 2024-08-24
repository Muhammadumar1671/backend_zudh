from django.urls import path
from . import views

app_name = 'authorization'

urlpatterns = [
    path('', views.signup, name='login'),
    path('login/', views.login, name='logout'),
    path ('verify/', views.verify_jwt_token, name='verify'),
    path('protected/', views.protected_endpoint, name='protected'),
    path('logout', views.logout, name='logout'),
]
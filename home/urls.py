from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
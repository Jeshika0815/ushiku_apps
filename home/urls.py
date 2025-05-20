from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('user/', views.user_profile, name='user_profile'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
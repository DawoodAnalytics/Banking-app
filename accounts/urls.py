from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/user/', views.user_login, name='user_login'),
    path('login/admin/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('manage/', views.admin_dashboard, name='admin_dashboard'),
]

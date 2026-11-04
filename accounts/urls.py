from django.urls import path
from . import views, admin_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/user/', views.user_login, name='user_login'),
    path('login/admin/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('manage/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('manage/promote/<int:pk>/', admin_views.promote_user, name='promote_user'),
    path('manage/toggle/<int:pk>/', admin_views.toggle_user, name='toggle_user'),
]

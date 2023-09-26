from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('create_post/', views.create_post, name='create_post'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('my-protected-view/', views.my_protected_view, name='my-protected-view'),
]

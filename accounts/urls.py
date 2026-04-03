from django.urls import path
from . import views

urlpatterns = [
    path('royxat/', views.register_view, name='register'),
    path('kirish/', views.login_view, name='login'),
    path('chiqish/', views.logout_view, name='logout'),
    path('profil/', views.profile_view, name='profile_own'),
    path('profil/tahrirlash/', views.profile_edit_view, name='profile_edit'),
    path('profil/<int:pk>/', views.profile_view, name='profile'),
]

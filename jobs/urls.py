from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('yaratish/', views.job_create_view, name='job_create'),
    path('<int:pk>/', views.job_detail_view, name='job_detail'),
    path('<int:pk>/tahrirlash/', views.job_edit_view, name='job_edit'),
    path('<int:pk>/ochirish/', views.job_delete_view, name='job_delete'),
    path('<int:pk>/ariza/', views.apply_job_view, name='apply_job'),
    path('ariza/<int:pk>/boshqarish/', views.manage_application_view, name='manage_application'),
    path('<int:pk>/tugallash/', views.complete_job_view, name='complete_job'),
    path('mening-ishlarim/', views.my_jobs_view, name='my_jobs'),
    path('mening-arizalarim/', views.my_applications_view, name='my_applications'),
]

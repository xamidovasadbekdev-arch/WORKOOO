from django.urls import path
from . import views

urlpatterns = [
    path('ish/<int:job_pk>/ishchi/<int:worker_pk>/baholash/', views.rate_worker_view, name='rate_worker'),
    path('ishchi/<int:pk>/baholar/', views.worker_ratings_view, name='worker_ratings'),
]

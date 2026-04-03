from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversation_list_view, name='conversation_list'),
    path('<int:pk>/', views.conversation_detail_view, name='conversation_detail'),
    path('<int:pk>/yuborish/', views.send_message_view, name='send_message'),
    path('<int:pk>/xabarlar/', views.get_messages_view, name='get_messages'),
]

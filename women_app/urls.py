from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('schemes/', views.schemes, name='schemes'),
     path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
    # API endpoint for AJAX chat (used by chatbot.js)
    path('api/chat/', views.chat_api, name='chat_api'),
]


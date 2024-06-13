from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('chat-rooms/', create_chat_room, name='create_chat_room'),
    path('chat-rooms/<int:pk>/', read_chat_room, name='read_chat_room'),
    path('chat-rooms/<int:pk>/update/', update_chat_room, name='update_chat_room'),
    path('chat-rooms/<int:chat_room_pk>/messages/', create_message, name='create_message'),
    path('chat-rooms/<int:chat_room_pk>/messages/search/', search_messages, name='search_messages'),
    path('chat-rooms/<int:chat_room_pk>/messages/<int:message_pk>/', read_message, name='read_message'),
    path('chat-rooms/<int:chat_room_pk>/messages/<int:message_pk>/update/', update_message, name='update_message'),
]
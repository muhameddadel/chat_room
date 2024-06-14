from django.urls import path
from .viewsets import ChatRoomViewSet, MessageViewSet

app_name = 'chat'

urlpatterns = [
    path('chat-rooms/', ChatRoomViewSet.as_view({'post': 'create'}), name='chatroom-create'),
    path('chat-rooms/<int:pk>/', ChatRoomViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='chatroom-detail'),
    path('chat-rooms/<int:chat_room_pk>/messages/', MessageViewSet.as_view({'post': 'create'}), name='message-create'),
    path('chat-rooms/<int:chat_room_pk>/messages/search/', MessageViewSet.as_view({'get': 'search'}), name='message-search'),
    path('chat-rooms/<int:chat_room_pk>/messages/<int:pk>/', MessageViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='message-detail'),
]

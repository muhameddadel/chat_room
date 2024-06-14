from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        return self.queryset.filter(chat_room_id=self.kwargs['chat_room_pk'])

    def create(self, request, *args, **kwargs):
        try:
            chat_room = ChatRoom.objects.get(pk=self.kwargs['chat_room_pk'])
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(chat_room=chat_room)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def search(self, request, chat_room_pk=None):
        query = request.query_params.get('q', '')
        chat_room = self.get_queryset().filter(content__icontains=query)
        page = self.paginate_queryset(chat_room)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(chat_room, many=True)
        return Response(serializer.data)

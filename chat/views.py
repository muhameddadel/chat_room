from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


############################### chatroom views ###############################
@api_view(['POST'])
def create_chat_room(request):
    serializer = ChatRoomSerializer(data=request.data)
    if serializer.is_valid():
        chat_room = serializer.save()
        return Response(ChatRoomSerializer(chat_room).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_chat_room(request, pk):
    try:
        chat_room = ChatRoom.objects.get(pk=pk)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChatRoomSerializer(chat_room, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def read_chat_room(request, pk):
    try:
        chat_room = ChatRoom.objects.get(pk=pk)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChatRoomSerializer(chat_room)
    return Response(serializer.data)


############################### messages views ###############################
@api_view(['POST'])
def create_message(request, chat_room_pk):
    try:
        chat_room = ChatRoom.objects.get(pk=chat_room_pk)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    content = request.data.get('content')
    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    message = Message(chat_room=chat_room, content=content)
    message.save()
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_message(request, chat_room_pk, message_pk):
    try:
        chat_room = ChatRoom.objects.get(pk=chat_room_pk)
        message = Message.objects.get(pk=message_pk, chat_room=chat_room)
    except (ChatRoom.DoesNotExist, Message.DoesNotExist):
        return Response({'error': 'Message or chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MessageSerializer(message, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def read_message(request, chat_room_pk, message_pk):
    try:
        chat_room = ChatRoom.objects.get(pk=chat_room_pk)
        message = Message.objects.get(pk=message_pk, chat_room=chat_room)
    except (ChatRoom.DoesNotExist, Message.DoesNotExist):
        return Response({'error': 'Message or chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MessageSerializer(message)
    return Response(serializer.data)

@api_view(['GET'])
def search_messages(request, chat_room_pk):
    try:
        chat_room = ChatRoom.objects.get(pk=chat_room_pk)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    query = request.query_params.get('q', '')
    messages = Message.objects.filter(chat_room=chat_room, content__icontains=query)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import ChatRoom, Message

class ChatRoomViewSetTests(APITestCase):
    def setUp(self):
        self.chat_room = ChatRoom.objects.create(title='Test Room')

    def test_create_chat_room(self):
        url = reverse('chat:chatroom-create')
        data = {'title': 'New Room'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 2)
        self.assertEqual(ChatRoom.objects.get(id=response.data['id']).title, 'New Room')

    def test_retrieve_chat_room(self):
        url = reverse('chat:chatroom-detail', kwargs={'pk': self.chat_room.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.chat_room.title)

    def test_partial_update_chat_room(self):
        url = reverse('chat:chatroom-detail', kwargs={'pk': self.chat_room.pk})
        data = {'title': 'Updated Room'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.chat_room.refresh_from_db()
        self.assertEqual(self.chat_room.title, 'Updated Room')


class MessageViewSetTests(APITestCase):
    def setUp(self):
        self.chat_room = ChatRoom.objects.create(title='Test Room')
        self.message = Message.objects.create(chat_room=self.chat_room, content='Test Message')

    def test_create_message(self):
        url = reverse('chat:message-create', kwargs={'chat_room_pk': self.chat_room.pk})
        data = {'content': 'New Message', 'chat_room': self.chat_room.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(Message.objects.get(id=response.data['id']).content, 'New Message')

    def test_retrieve_message(self):
        url = reverse('chat:message-detail', kwargs={'chat_room_pk': self.chat_room.pk, 'pk': self.message.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.message.content)

    def test_partial_update_message(self):
        url = reverse('chat:message-detail', kwargs={'chat_room_pk': self.chat_room.pk, 'pk': self.message.pk})
        data = {'content': 'Updated Message'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        self.assertEqual(self.message.content, 'Updated Message')

    def test_search_messages(self):
        url = reverse('chat:message-search', kwargs={'chat_room_pk': self.chat_room.pk})
        response = self.client.get(url, {'q': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Test Message')

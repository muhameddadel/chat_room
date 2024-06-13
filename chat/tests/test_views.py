from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import ChatRoom, Message
from ..serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomTests(APITestCase):

    def setUp(self):
        self.chat_room = ChatRoom.objects.create(title='Test Room')
        self.message = Message.objects.create(chat_room=self.chat_room, content='Test Message')
        self.valid_chat_room_data = {'title': 'New Room'}
        self.valid_message_data = {'content': 'New Message'}
        self.invalid_message_data = {'content': ''}

    def test_create_chat_room(self):
        url = reverse('chat:create_chat_room')
        response = self.client.post(url, self.valid_chat_room_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 2)

    def test_update_chat_room(self):
        url = reverse('chat:update_chat_room', args=[self.chat_room.id])
        updated_title = 'Updated Room'
        data = {'title': updated_title}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.chat_room.refresh_from_db()
        self.assertEqual(self.chat_room.title, updated_title)

    def test_read_chat_room(self):
        url = reverse('chat:read_chat_room', args=[self.chat_room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.chat_room.title)

    def test_create_message(self):
        url = reverse('chat:create_message', args=[self.chat_room.id])
        response = self.client.post(url, self.valid_message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)

    def test_update_message(self):
        url = reverse('chat:update_message', args=[self.chat_room.id, self.message.id])
        updated_content = 'Updated Message'
        data = {'content': updated_content}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        self.assertEqual(self.message.content, updated_content)

    def test_read_message(self):
        url = reverse('chat:read_message', args=[self.chat_room.id, self.message.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.message.content)

    def test_search_messages(self):
        url = reverse('chat:search_messages', args=[self.chat_room.id])
        query = 'Test'
        response = self.client.get(url, {'q': query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(query.lower() in msg['content'].lower() for msg in response.data))

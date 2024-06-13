from rest_framework.test import APITestCase
from ..models import ChatRoom, Message

class ChatRoomModelTestCase(APITestCase):
    
    def setUp(self):
        self.chatroom = ChatRoom.objects.create(title="Test Chat Room")

    def test_chatroom_creation(self):
        self.assertTrue(isinstance(self.chatroom, ChatRoom))
        self.assertEqual(self.chatroom.__str__(), f"Chat Room {self.chatroom.id}")
    
    def test_message_creation(self):
        message = Message.objects.create(chat_room=self.chatroom, content="Test message")
        self.assertTrue(isinstance(message, Message))
        self.assertEqual(message.__str__(), f"Message {message.id} in {self.chatroom}")

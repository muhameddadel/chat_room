## run using docker

### To build the container

- docker-compose -f docker-compose.yml up --build -d

### To migrate with docker

- docker exec -it django python manage.py migrate

### To makemigrations with docker

- docker exec -it django python manage.py makemigrations

## API Endpoints

### Chat Rooms:
        - POST /chat-rooms/ - Create a new chat room.
        - GET /chat-rooms/<int:pk>/ - Retrieve a specific chat room.
        - PATCH /chat-rooms/<int:pk>/ - Update a specific chat room.

### Messages:

        - POST /chat-rooms/<int:chat_room_pk>/messages/ - Create a new message in a chat room.
        - GET /chat-rooms/<int:chat_room_pk>/messages/<int:pk>/ - Retrieve a specific message.
        - PATCH /chat-rooms/<int:chat_room_pk>/messages/<int:pk>/ - Update a specific message.
        - GET /chat-rooms/<int:chat_room_pk>/messages/search/?q=<query> - Search for messages in a chat room.
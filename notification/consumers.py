import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"] is AnonymousUser() or not self.scope["user"].is_authenticated:
            await self.close()
        else:
            self.user = self.scope["user"]
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Optional: Receive data from WebSocket (e.g., mark notification as read).
        """
        data = json.loads(text_data)
        notification_id = data.get('notification_id')
        if notification_id:
            await self.mark_as_read(notification_id)

    @database_sync_to_async
    def mark_as_read(self, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=self.user)
            notification.is_read = True
            notification.save()
        except Notification.DoesNotExist:
            pass

    async def send_notification(self, event):
        """
        Called when a notification is sent to the group.
        """
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'timestamp': event['timestamp'],
        }))
# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        message = event['message']
        event_type = event.get('type', 'unknown')

        if event_type == 'send_notification':
            article_data = event.get('article_data', {})
            await self.send(text_data=json.dumps({
                'message': message,
                'article_data': article_data,
            }))
        elif event_type == 'delete_article':
            await self.delete_article(event)

    async def delete_article(self, event):
        message = event['message']
        article_id = event.get('article_id', 'Unknown')
        await self.send(text_data=json.dumps({
            'message': message,
            'article_id': article_id
        }))
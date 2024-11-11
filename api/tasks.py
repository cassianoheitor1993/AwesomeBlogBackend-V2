from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Article

@shared_task
def send_article_notification_task(article_id):
    article = Article.objects.get(id=article_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": "New article",
            "article_data": article.get_data(),
        }
    )
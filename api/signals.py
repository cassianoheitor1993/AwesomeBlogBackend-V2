# api/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Article
import logging

logger = logging.getLogger(__name__)
deleted_article_ids = []
@receiver(post_delete, sender=Article)
def collect_deleted_article_ids(sender, instance, **kwargs):
    global deleted_article_ids
    deleted_article_ids.append(instance.id)

@receiver(post_save, sender=Article)
def send_article_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    message = "New article" if created else "Updated article"
    print(f"Sending notification: {message}")
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": message,
            "article_data": instance.get_data(),
        }
    )

@receiver(post_delete, sender=Article)
def send_article_deletion_notification(sender, instance, **kwargs):
    global deleted_article_ids
    if len(deleted_article_ids) > 0:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "delete_article",
                "message": "Article deleted",
                "article_id": deleted_article_ids
            }
        )
        deleted_article_ids = []

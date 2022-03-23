from django.db.models.signals import post_save
from django.dispatch import receiver
from articles.models import PublishedPost, PublishedVideo
from .tasks import start_post_publicator, start_video_publicator


@receiver(post_save, sender=PublishedPost)
def post_publicator(instance, **kwargs):
    start_post_publicator.delay(instance.id)


@receiver(post_save, sender=PublishedVideo)
def video_publicator(instance, **kwargs):
    start_video_publicator.delay(instance.id)

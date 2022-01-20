import django.dispatch

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from articles.models import PublishedPost
from .tasks import start_post_publicator


publish = django.dispatch.Signal()


@receiver(publish, sender=PublishedPost)
@receiver(post_save, sender=PublishedPost)
def post_publicator(instance, **kwargs):
    start_post_publicator.delay(instance.id)

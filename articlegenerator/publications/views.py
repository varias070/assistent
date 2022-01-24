from .signals import publish
from .tasks import start_post_publicator


def publish(request):
    start_post_publicator(request.id)

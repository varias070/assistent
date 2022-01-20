from .signals import publish


def publish():
    publish.send()

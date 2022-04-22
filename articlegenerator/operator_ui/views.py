from django.http import HttpResponseRedirect

from publications.tasks import start_post_publicator, start_article_publicator, start_video_publicator
from articles.models import PublishedPost, PublishedArticle, PublishedVideo
from django.shortcuts import get_object_or_404


def publish_post(request, pk):
    obj = get_object_or_404(PublishedPost, pk=pk)
    start_post_publicator.delay(obj.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def publish_article(request, pk):
    obj = get_object_or_404(PublishedArticle, pk=pk)
    start_article_publicator.delay(obj.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def publish_video(request, pk):
    obj = get_object_or_404(PublishedVideo, pk=pk)
    start_video_publicator.delay(obj.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
